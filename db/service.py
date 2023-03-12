from http import HTTPStatus
from bottle import abort
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


class Service:
    
    def __init__(self, dbhelper: DbHelper, model: Model):
        self.dbhelper = dbhelper
        self.model = model
    
    
    def get_all_records(self) -> list:
        self.__check_model()
        fields = ', '.join([f.name for f in self.model.fields])
        sql = f'select {fields} from {self.model.table};'
        ok, rows = self.dbhelper.query(sql)
        if not ok:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        return rows
        
    
    def get_record_by_id(self, pk: int) -> dict:
        self.__check_model()
        fields = ', '.join([f.name for f in self.model.fields])
        sql = f'''select {fields} 
            from {self.model.table} 
            where {self.model.pk.name} = {pk};'''
        ok, rows = self.dbhelper.query(sql)
        if not ok:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        if not rows:
            abort(HTTPStatus.NOT_FOUND, f'No element found with {self.model.pk.name} {pk}')
        return rows[0]


    def insert_record(self, record_data: dict) -> int:
        self.__check_model()
        try:
            self.model.from_dict(record_data)
            col_list = []
            val_list = []
            params = []
            for field in self.model.fields:
                if not field.pk:
                    self.__check_integrity(field)
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
        self.__check_model()
        try:
            self.model.from_dict(record_data)
            setlist = []
            params = []
            for field in self.model.fields:
                if not field.pk:
                    self.__check_integrity(field)
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
                abort(HTTPStatus.NOT_FOUND)
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
            abort(HTTPStatus.NOT_FOUND)


    def __check_model(self):
        if not self.model.fields:
            log('The given model has no fields', 'ERROR')
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
        if not self.model.pk:
            log('The given model has no primary key', 'ERROR')
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    

    def __check_integrity(self, field: Field):
        if field.unique:
            sql = f'''select count(*) as count from {self.model.table} 
                where {field.name} = ?;'''
            ok, rows = self.dbhelper.query(sql, (self.model.obj[field.name],))
            if not ok:
                raise ApiError()
            if rows and rows[0]['count'] >= 1:
                raise ApiError(HTTPStatus.BAD_REQUEST, f'Given value for "{field.name}" already exists')
            