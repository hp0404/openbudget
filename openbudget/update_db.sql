SELECT TOP 0 * INTO #tt FROM [Budget].[dbo].[OpenBudgetIncomes]

BULK INSERT #tt
FROM 'd:\openbudget\data\INCOMES_2020-08-01.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',  --CSV field delimiter
    ROWTERMINATOR = '\n',   --Use to shift the control to next row
    TABLOCK
)

INSERT INTO [Budget].[dbo].[OpenBudgetIncomes]
SELECT * FROM #tt
