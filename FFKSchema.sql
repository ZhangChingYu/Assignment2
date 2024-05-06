DROP TABLE IF EXISTS MenuItem;
DROP TABLE IF EXISTS MilkKind;
DROP TABLE IF EXISTS CoffeeType;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Staff;
DROP FUNCTION IF EXISTS SEARCH_BY_KEYWORD;
DROP FUNCTION IF EXISTS SORTED_KEYWORD_RESULTS;

CREATE TABLE Staff
(
	StaffID		VARCHAR(10)		PRIMARY KEY,
	Password	VARCHAR(30)		NOT NULL,
	FirstName	VARCHAR(30)		NOT NULL,
	LastName	VARCHAR(30)		NOT NULL,
	Age			INTEGER			NOT NULL CHECK (Age > 21),
	Salary		DECIMAL(9,2)	NOT NULL CHECK (Salary > 0)
);

CREATE TABLE Category
(
	CategoryID		SERIAL	PRIMARY KEY,
	CategoryName	VARCHAR(10) UNIQUE NOT NULL,
	CategoryDesc	VARCHAR(40)	NOT NULL
);

CREATE TABLE CoffeeType
(
	CoffeeTypeID	SERIAL	PRIMARY KEY,
	CoffeeTypeName	VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE MilkKind
(
	MilkKindID		SERIAL	PRIMARY KEY,
	MilkKindName	VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE MenuItem
(
	MenuItemID		SERIAL			PRIMARY KEY,
	Name			VARCHAR(30)		NOT NULL,
	Description		VARCHAR(150),
	CategoryOne		INTEGER			NOT NULL REFERENCES Category,
	CategoryTwo		INTEGER			REFERENCES Category,
	CategoryThree	INTEGER			REFERENCES Category,
	CoffeeType		INTEGER			REFERENCES CoffeeType,
	MilkKind		INTEGER			REFERENCES MilkKind,
	Price			DECIMAL(6,2)	NOT NULL,
	ReviewDate		DATE,
	Reviewer		VARCHAR(10) 	REFERENCES Staff
);

CREATE OR REPLACE FUNCTION get_category_id(category_name VARCHAR) 
RETURNS INTEGER AS $$
DECLARE
	category_id INTEGER;
BEGIN
	SELECT CategoryID INTO category_id
	FROM Category
	WHERE LOWER(CategoryName)=LOWER(category_name);
	RETURN category_id;
END;$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_coffee_type_id(coffee_type_name VARCHAR) 
RETURNS INTEGER AS $$
DECLARE
	coffee_type_id INTEGER;
BEGIN
	SELECT CoffeeTypeID INTO coffee_type_id
	FROM CoffeeType
	WHERE LOWER(CoffeeTypeName)=LOWER(coffee_type_name);
	RETURN coffee_type_id;
END;$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_milk_kind_id(milk_kind_name VARCHAR) 
RETURNS INTEGER AS $$
DECLARE
	milk_kind_id INTEGER;
BEGIN
	SELECT MilkKindID INTO milk_kind_id
	FROM MilkKind
	WHERE LOWER(MilkKindName)=LOWER(milk_kind_name);
	RETURN milk_kind_id;
END;$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_menu_item(n_name VARCHAR, n_description VARCHAR, catergory1 INTEGER,
										category2 INTEGER, category3 INTEGER, coffee_id INTEGER, 
										milk_id INTEGER, price DECIMAL)
RETURNS VOID AS $$
BEGIN
	INSERT INTO MenuItem(Name, Description, CategoryOne, CategoryTwo, CategoryThree, CoffeeType, MilkKind, Price)
	VALUES (n_name, n_description, catergory1, category2, category3, coffee_id, milk_id, price);
END;$$ LANGUAGE plpgsql;

SET datestyle to 'ISO, DMY';

INSERT INTO Staff VALUES ('ajones','098','Anna','Jones',25,41000);
INSERT INTO Staff VALUES ('ganderson','987','Glen','Anderson',30,49500.80);
INSERT INTO Staff VALUES ('jwalker','876','James','Walker',22,38890.50);
INSERT INTO Staff VALUES ('janedoe','765','Jane','Doe',26,43900.20);
INSERT INTO Staff VALUES ('johndoe','654','John','Doe',22,38000);
INSERT INTO Staff VALUES ('njohnson','543','Neil','Johnson',27,4500);
INSERT INTO Staff VALUES ('nbrown','432','Nicole','Brown',41,68100.90);
INSERT INTO Staff VALUES ('rtatum','321','Robert','Tatum',39,62400);
INSERT INTO Staff VALUES ('rmarrick','210','Ryu','Marrick',36,59900.20);
INSERT INTO Staff VALUES ('tcolemen','109','Tom','Coleman',24,48000);

INSERT INTO Category VALUES (1,'Breakfast','Menu item to be offered for breakfast');
INSERT INTO Category VALUES (2,'Lunch','Menu item to be offered for lunch');
INSERT INTO Category VALUES (3,'Dinner','Menu item to be offered for dinner');

INSERT INTO CoffeeType VALUES (1,'Espresso');
INSERT INTO CoffeeType VALUES (2,'Latte');
INSERT INTO CoffeeType VALUES (3,'Cappuccino');
INSERT INTO CoffeeType VALUES (4,'LongBlack');
INSERT INTO CoffeeType VALUES (5,'ColdBrew');

INSERT INTO MilkKind VALUES (1,'Whole');
INSERT INTO MilkKind VALUES (2,'Skim');
INSERT INTO MilkKind VALUES (3,'Soy');
INSERT INTO MilkKind VALUES (4,'Almond');
INSERT INTO MilkKind VALUES (5,'Oat');

SET datestyle to 'ISO, DMY';

INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('French Toast','A sliced bread soaked in beaten eggs, milk, and cream, then pan-fried with butter',1,NULL,NULL,NULL,NULL,9.90,'10/01/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Eggs Benedict','An English muffin, toasted, and topped with bacon, poached eggs, and classic French hollandaise sauce',1,2,NULL,NULL,NULL,12.80,'18/02/2024','janedoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Poke Bowl','Cubes of marinated fish tossed over rice and topped with vegetables and Asian-inspired sauces',1,2,3,NULL,NULL,15.90,'28/02/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Orange Juice','A fresh, sweet, and juicy drink with orange bits made from freshly squeezed oranges',1,2,3,NULL,NULL,6.50,'01/03/2024','janedoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('White Coffee','A full-flavored concentrated form of coffee served in small, strong shots with whole milk',1,2,NULL,1,1,3.50,'22/03/2024','rtatum');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Black Coffee',NULL,1,2,3,4,NULL,4.30,NULL,NULL);
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Coffee Drink',NULL,1,2,NULL,3,3,3.50,'28/02/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Seafood Cleopatra','Salmon topped with prawns in a creamy seafood sauce. Served with salad and chips',3,NULL,NULL,NULL,NULL,25.90,'20/02/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Iced Coffee','A glass of cold espresso, milk, ice cubes, and a scoop of ice cream',1,2,NULL,2,1,7.60,NULL,NULL);
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Coffee Pancake','A short stack of pancakes flecked with espresso powder and mini chocolate chips',1,NULL,NULL,NULL,NULL,8.95,'08/04/2014','janedoe');
	
	
CREATE FUNCTION SEARCH_BY_KEYWORD(IN keyword VARCHAR)
RETURNS TABLE(
	mid INTEGER, 
	Name VARCHAR, 
	Description VARCHAR, 
	categoryOne VARCHAR, 
	categoryTwo VARCHAR, 
	categoryThree VARCHAR, 
	coffeeType VARCHAR, 
	milkType VARCHAR, 
	price NUMERIC(6,2), 
	reviewDate DATE, 
	reviewer VARCHAR
) AS $$
BEGIN
	RETURN QUERY
	SELECT 
		mi.menuItemId,
		mi.Name,
		mi.description,
		c1.categoryName, 
		c2.categoryName,
		c3.categoryName,
		ct.coffeeTypeName,
		mk.milkKindName,
		mi.price,
		mi.reviewDate,
		cast(concat(s.firstname,' ',s.lastname) as VARCHAR)
	FROM MenuItem mi
	LEFT JOIN Category AS c1 ON mi.categoryOne = c1.categoryId
	LEFT JOIN Category AS c2 ON mi.categoryTwo = c2.categoryId 
	LEFT JOIN Category AS c3 ON mi.categoryThree = c3.categoryId
	LEFT JOIN CoffeeType AS ct ON mi.coffeeType = ct.coffeeTypeId
	LEFT JOIN MilkKind AS mk ON mi.milkKind = mk.milkKindId
	LEFT JOIN Staff AS s ON mi.reviewer = s.StaffID
	WHERE LOWER(mi.Name) LIKE ('%' || LOWER(keyword) || '%')
	OR (LOWER(s.firstName)||' '|| LOWER(s.lastName)) LIKE ('%' || LOWER(keyword) || '%')
	OR LOWER(mi.description) LIKE ('%' || LOWER(keyword) || '%')
	OR LOWER(mi.reviewer) LIKE ('%' || LOWER(keyword) || '%')
	OR LOWER(c1.categoryName) LIKE ('%' || LOWER(keyword) || '%')
	OR LOWER(c2.categoryName) LIKE ('%' || LOWER(keyword) || '%')
	OR LOWER(c3.categoryName) LIKE ('%' || LOWER(keyword) || '%');
END; $$
LANGUAGE plpgsql;

CREATE FUNCTION SORTED_KEYWORD_RESULTS(IN keyword VARCHAR)
RETURNS TABLE(
	mid INTEGER, 
	Name VARCHAR, 
	Description VARCHAR, 
	categoryOne VARCHAR, 
	categoryTwo VARCHAR, 
	categoryThree VARCHAR, 
	coffeeType VARCHAR, 
	milkType VARCHAR, 
	price NUMERIC(6,2), 
	reviewDate DATE, 
	reviewer VARCHAR
) AS $$
BEGIN
	RETURN QUERY
	SELECT * FROM SEARCH_BY_KEYWORD(keyword) sbk
	WHERE sbk.reviewDate >= CURRENT_DATE - INTERVAL '10 years'
	OR sbk.reviewDate IS null
	ORDER BY reviewer ASC, reviewDate DESC;
END; $$
LANGUAGE plpgsql;

COMMIT;
