
--409856043 Tony Siu Database final exam doc A
--1

--2
--a
--first normal form
--b
--transitive dependency
--3
--a
CREATE TABLE sales_t(
    EID VARCHAR(10),
    EmployeeName VARCHAR(25),
    SalespersonPhone VARCHAR(50),
    EmpType VARCHAR(20),
    TerritoryID NUMBER(11,0),
    CONSTRAINT pk PRIMARY KEY (EID),
    CONSTRAINT fk FOREIGN KEY territory_t(TerritoryID),
    CHECK (EmpType IN ("FullTime","PartTime"))
);
--b
ALTER TABLE sales_t ADD  salesperson VARCHAR(10);
--c
SELECT *
FROM Product_T
WHERE ProductFinish IN ('Cherry','Natural Ash')
ORDER BY ProductFinish DESC;
--e
SELECT *
FROM Customer_T,Order_T
WHERE Customer_T.CustomerID != Order_T.CustomerID
ORDER BY CustomerState,CustomerName;
--f comback
SELECT OrderID,sum(Product_T.ProductStandardPrice * OrderLine_T.OrderedQuantity) AS totalprice
FROM OrderLine_T
INNER JOIN Product_T
    ON OrderLine_T.ProductID = Product_T.ProductID
GROUP BY OrderID
HAVING totalprice > 2000;
    
--g
CREATE VIEW BigOrder AS 
SELECT OrderID,sum(Product_T.ProductStandardPrice * OrderLine_T.OrderedQuantity) AS totalprice
FROM OrderLine_T
INNER JOIN Product_T
    ON OrderLine_T.ProductID = Product_T.ProductID
GROUP BY OrderID
HAVING totalprice > 2000;

--h
SELECT *--name.CustomerName
FROM BigOrder,Order_T,(SELECT CustomerName,CustomerID FROM Customer_T) AS name
WHERE BigOrder.OrderID = Order_T.OrderID 
    AND name.CustomerID = Order_T.CustomerID
    
 
    
    