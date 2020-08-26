import os
print('__file__', __file__)
print('dirname', os.path.dirname(__file__))
print('abspath', os.path.abspath(os.path.dirname(__file__))

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.join(basedir, 'app.db'))
