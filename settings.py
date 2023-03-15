class Config:
  __conf = {
    # muttable
    'DB_NAME': 'dronery.db',
    'TESTING': False,

    # constants
    'LOW_LEVEL': 25,
    'AUDIT_DELTA_SECONDS': 20, # seconds between audits
  }
  __setters = ['DB_NAME', 'TESTING']

  @staticmethod
  def get(name):
    return Config.__conf[name]

  @staticmethod
  def set(name, value):
    if name in Config.__setters:
      Config.__conf[name] = value
    else:
      raise NameError('Name not accepted in set() method')
