'''
file: car_db.py
date: 2/18/14
desc: built the tables for the database
'''
import random
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

# database engine, declarative base, and session factory
db_engine = sqlalchemy.create_engine(
	'mysql://root:jimn42@localhost:3306/car_db',
	isolation_level = 'SERIALIZABLE',
	echo = True)
db_base = sqlalchemy.ext.declarative.declarative_base()
db_session = sqlalchemy.orm.sessionmaker()

# database tables
class CarInformation(db_base):
	'''
		The car_information table defines the information associated
		to the car, such as model number, performance, and etc.
	'''
	__tablename__ = 'car_information'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	car_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	car_make = sqlalchemy.Column(sqlalchemy.String(255))
	car_model = sqlalchemy.Column(sqlalchemy.String(255))
	car_year = sqlalchemy.Column(sqlalchemy.String(255))
	car_retail = sqlalchemy.Column(sqlalchemy.String(255))
	car_maintenance = sqlalchemy.Column(sqlalchemy.String(255))
	car_warranty = sqlalchemy.Column(sqlalchemy.String(255))
	car_premium = sqlalchemy.Column(sqlalchemy.String(255))
	comp_perf = sqlalchemy.orm.relationship('CompPerformance')
	comp_hand = sqlalchemy.orm.relationship('CompHandling')
	comp_inst = sqlalchemy.orm.relationship('CompInstrument')
	comp_safe = sqlalchemy.orm.relationship('CompSafety')
	comp_secu = sqlalchemy.orm.relationship('CompSecurity')
	comp_extr = sqlalchemy.orm.relationship('CompExterior')
	comp_intr = sqlalchemy.orm.relationship('CompInterior')
	comp_audo = sqlalchemy.orm.relationship('CompAudio')
	comp_luxr = sqlalchemy.orm.relationship('CompLuxury')
	comp_pack = sqlalchemy.orm.relationship('CompPackage')

def CarInventory(db_base):
	'''
		The car_inventory table defines the list of cars that 
		are in the inventory and catalog, which is viewable by 
		customers.
	'''
	__tablename__ = 'car_inventory'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	inv_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	car_cid = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey('car_information.car_id'))
	car_info = sqlalchemy.orm.relationship('CarInformation')


'''	
[Description]
	The component series serves as a child to car information providing
	the specific type and detail of the component in relation to some 
	property.
[Paramater]
	xyz_id		- distinct ID
	xyz_type 	- type of component within property
	xyz_desc 	- specific detail of component within property
'''
class CompPerformance(db_base):
	__tablename__ = 'comp_performance'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	perf_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	perf_type = sqlalchemy.Column(sqlalchemy.String(255))
	perf_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompHandling(db_base):
	__tablename__ = 'comp_handling'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	hand_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	hand_type = sqlalchemy.Column(sqlalchemy.String(255))
	hand_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompInstrument(db_base):
	__tablename__ = 'comp_instrument'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	inst_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	inst_type = sqlalchemy.Column(sqlalchemy.String(255))
	inst_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompSafety(db_base):
	__tablename__ = 'comp_safety'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	safe_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	safe_type = sqlalchemy.Column(sqlalchemy.String(255))
	safe_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompSecurity(db_base):
	__tablename__ = 'comp_security'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	secu_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	secu_type = sqlalchemy.Column(sqlalchemy.String(255))
	secu_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompExterior(db_base):
	__tablename__ = 'comp_exterior'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	extr_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	extr_type = sqlalchemy.Column(sqlalchemy.String(255))
	extr_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompInterior(db_base):
	__tablename__ = 'comp_interior'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	intr_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	intr_type = sqlalchemy.Column(sqlalchemy.String(255))
	intr_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompAudio(db_base):
	__tablename__ = 'comp_audio'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	audo_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	audo_type = sqlalchemy.Column(sqlalchemy.String(255))
	audo_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompLuxury(db_base):
	__tablename__ = 'comp_luxury'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	luxr_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	luxr_type = sqlalchemy.Column(sqlalchemy.String(255))
	luxr_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))
class CompPackage(db_base):
	__tablename__ = 'comp_package'
	__table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
	pack_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement = True)
	pack_type = sqlalchemy.Column(sqlalchemy.String(255))
	pack_desc = sqlalchemy.Column(sqlalchemy.String(255))
	car_pid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('car_information.car_id'))

# Generator Set Functions
def randstr():
	return ''.join([chr(random.randint(0,25) + 65) for i in range(10)])

def generate_car(current_session):
	test_car = CarInformation(	car_make = randstr(), car_model = randstr(), car_year = randstr(),
								car_retail = randstr(), car_maintenance = randstr(), car_warranty = randstr(), 
								car_premium = randstr());
	test_car.comp_perf = [CompPerformance(perf_type = randstr(), perf_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_hand = [CompHandling(hand_type = randstr(), hand_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_inst = [CompInstrument(inst_type = randstr(), inst_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_safe = [CompSafety(safe_type = randstr(), safe_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_secu = [CompSecurity(secu_type = randstr(), secu_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_extr = [CompExterior(extr_type = randstr(), extr_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_intr = [CompInterior(intr_type = randstr(), intr_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_audo = [CompAudio(audo_type = randstr(), audo_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_luxr = [CompLuxury(luxr_type = randstr(), luxr_desc = randstr()) for i in range(random.randint(1,3))]
	test_car.comp_pack = [CompPackage(pack_type = randstr(), pack_desc = randstr()) for i in range(random.randint(1,3))]
	current_session.add(test_car)

if __name__ == '__main__':
	# Create the table in the database
	db_base.metadata.bind = db_engine
	db_base.metadata.create_all()

	# Initial the tables with some data
	init_session = db_session()
	for count in range(10): generate_car(init_session)
	init_session.commit()
