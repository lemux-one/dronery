from http import HTTPStatus
from bottle import (
    abort,
    MultiDict
)
from db.db_helper import (
    DbHelper,
    DbError
)
from db.model import (
    Model,
    Field
)
from api.utils import (
    log,
    ApiError
)

NO_RECORD_MESSAGE = 'Record does not exist'
ALLOWED_COMPARISON_OPERATORS = ('=', '<=', '>=', '<>', '!=', '<', '>', 'in', 'between',)
ALLOWED_BOOLEAN_OPERATORS = ('and',)

class Service:
    
    def __init__(self, dbhelper: DbHelper, model: Model):
        self.dbhelper = dbhelper
        self.model = model
    
    
    def get_all_records(self, filters: MultiDict = None) -> list:
        self.check_model()
        fields = ', '.join([f.name for f in self.model.fields])
        sql = f'select {fields} from {self.model.table}'
        sql_filter, params = self.__prepare_sql_from_filters(filters)
        if sql_filter:
            sql += f' where 1=1 {sql_filter}'
        ok, rows = self.dbhelper.query(sql, params)
        if not ok:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        return rows
        
    
    def get_record_by_id(self, pk: int) -> dict:
        self.check_model()
        fields = ', '.join([f.name for f in self.model.fields])
        sql = f'''select {fields} 
            from {self.model.table} 
            where {self.model.pk.name} = {pk};'''
        ok, rows = self.dbhelper.query(sql)
        if not ok:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        if not rows:
            abort(HTTPStatus.NOT_FOUND, NO_RECORD_MESSAGE)
        return rows[0]


    def insert_record(self, record_data: dict) -> int:
        self.check_model()
        try:
            self.model.from_dict(record_data)
            col_list = []
            val_list = []
            params = []
            for field in self.model.fields:
                if not field.pk:
                    self.check_constraints(field)
                    col_list.append(field.name)
                    val_list.append('?')
                    params.append(self.model.obj[field.name])
            sql = f'''insert into {self.model.table} ({', '.join(col_list)})
                values({', '.join(val_list)});'''
            ok, info = self.dbhelper.exec(sql, params)
            if ok:
                return info['last_id']
            else:
                raise DbError(f'Insert in "{self.model.table}" failed')
        except ValueError as ex:
            log(str(ex), 'ERROR')
            abort(HTTPStatus.BAD_REQUEST, str(ex))
        except ApiError as ex:
            abort(ex.status_code, ex.message)


    def update_record_by_id(self, pk: int, record_data: dict) -> None:
        self.check_model()
        try:
            self.model.from_dict(record_data)
            setlist = []
            params = []
            for field in self.model.fields:
                if not field.pk:
                    self.check_constraints(field, exclude_pk=pk)
                    setlist.append(f'{field.name} = ?')
                    params.append(self.model.obj[field.name])
            sql = f'''update {self.model.table} 
                set {', '.join(setlist)} 
                where {self.model.pk.name} = ?;'''
            params.append(pk)
            ok, info = self.dbhelper.exec(sql, params)
            if not ok:
                raise DbError(f'Update in "{self.model.table}" failed')
            if info['row_count'] < 1:
                abort(HTTPStatus.NOT_FOUND, NO_RECORD_MESSAGE)
        except ValueError as ex:
            log(str(ex), 'ERROR')
            abort(HTTPStatus.BAD_REQUEST, str(ex))
        except ApiError as ex:
            abort(ex.status_code, ex.message)
    

    def delete_by_id(self, pk: int) -> None:
        sql = f'''delete from {self.model.table}
            where {self.model.pk.name} = ?;'''
        ok, info = self.dbhelper.exec(sql, (pk,))
        if not ok:
            log(f'Delete from {self.model.table} failed', 'ERROR')
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        if info['row_count'] < 1:
            abort(HTTPStatus.NOT_FOUND, NO_RECORD_MESSAGE)


    def check_model(self):
        if not self.model.fields:
            log('The given model has no fields', 'ERROR')
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        if not self.model.pk:
            log('The given model has no primary key', 'ERROR')
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    

    def check_constraints(self, field: Field, exclude_pk: int = None):
        if field.unique:
            self.__check_unique(field, exclude_pk)
        if field.fk:
            self.__check_fk(field)
    

    def __check_unique(self, field: Field, exclude_pk: int):
        params = []
        sql = f'''select count(*) as count from {self.model.table} 
            where {field.name} = ?'''
        params.append(self.model.obj[field.name])
        if exclude_pk is not None:
            sql += f' and {self.model.pk.name} <> ?'
            params.append(exclude_pk)
        ok, rows = self.dbhelper.query(sql, params)
        if not ok:
            raise ApiError()
        if rows and rows[0]['count'] >= 1:
            raise ApiError(HTTPStatus.BAD_REQUEST, f'Given value for "{field.name}" already exists')
            
    
    def __check_fk(self, field: Field):
        if not field.ftable or not self.dbhelper.exists_table(field.ftable):
            raise ApiError(message=f'Invalid ftable={str(field.ftable)} for FK "{field.name}"')
        sql = f'select count(*) as count from {field.ftable} where {field.name} = ?'
        ok, rows = self.dbhelper.query(sql, [self.model.obj[field.name]])
        if not ok:
            raise ApiError()
        if not rows or rows[0]['count'] != 1:
            raise ApiError(message=f'Invalid FK "{field.name}"')
    
    def __prepare_sql_from_filters(self, filters: MultiDict) -> (str, list):
        params = []
        sql_filter = ''
        if filters:
            field_names = [field.name for field in self.model.fields]
            for filter in filters:
                bool_operator, filter_by = self.__extract_from_target(filter)
                if filter_by in field_names:
                    requirements = filters.getall(filter)
                    for req in requirements:
                        comparator, criteria = self.__extract_from_requirement(req)
                        placeholders = []
                        for val in criteria:
                            params.append(val)
                            placeholders.append('?')
                        placeholders = ','.join(placeholders)
                        sql_filter += f' {bool_operator} {filter_by} {comparator} ({placeholders})'
        return sql_filter, params

    def __extract_from_requirement(self, requirement: str) -> (str, [str]):
        criteria = requirement
        comparator = '='
        if str(requirement).startswith('['):
            splitted = str(requirement)[1:].split(']')
            if len(splitted) != 2:
                abort(HTTPStatus.BAD_REQUEST, f'Malformed filter requirement {requirement}')
            comparator, criteria = splitted
            if comparator not in ALLOWED_COMPARISON_OPERATORS:
                abort(HTTPStatus.BAD_REQUEST, f'Invalid comparison operator {comparator}')
            criteria = [item.strip() for item in criteria.split(',')]
        return comparator, criteria
    

    def __extract_from_target(self, target_field: str) -> (str, str):
        bool_operator = 'and'
        target = target_field
        if str(target_field).startswith('['):
            splitted = str(target_field)[1:].split(']')
            if len(splitted) != 2:
                abort(HTTPStatus.BAD_REQUEST, f'Malformed filter target field {target_field}')
            bool_operator, target = splitted
            if bool_operator not in ALLOWED_BOOLEAN_OPERATORS:
                abort(HTTPStatus.BAD_REQUEST, f'Invalid boolean operator {bool_operator}')
        return bool_operator, target
