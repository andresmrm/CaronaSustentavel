from setuptools import setup

setup(name='carona', version='1.0',
      description='Um site muito fera de caronas',
      author='Andres MRM', author_email='andresmrm@gmail.com ',
      url='http://www.python.org/sigs/distutils-sig/',

      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=['greenlet', 'gevent',
                        #  'MySQL-python',
                        #  'pymongo',
                        #  'psycopg2',
      ],
     )
