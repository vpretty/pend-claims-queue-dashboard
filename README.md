# Pended Claims Queue Dashboard
This is an example ETL pipeline and PowerBI dashboard based on an actual project I completed during my tenure at Commonwealth Care Alliance during the fall of 2024. To abide with relevant NDAs, certain aspects of this project have been changed from the original.

This project uses synthetic Medicare claims data provided by CMS. You can find this dataset at:
https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-20

## Background
Commonwealth Care Alliance is a healthcare services organization which provides care delivery and health plans for Medicare and Medicaid recipients in the New England area. During my tenure there, I was tasked with creating a data dashboard to report metrics surrounding pending medical claims.

Medical claims can pend for a variety of reasons. While CCA had multiple different queues for pended claims, for simplicity's sake, this project outline only focuses on the primary pending claims queue.

## ETL Pipeline Overview


On a regularly scheduled basis, a pipeline I wrote extracted pending claims data from CCA's claims management systems database. This data was loaded into a pandas dataframe for transformation. After being formatted, certain fields were used to query CCA's provider database to pull additional data about rendering providers and service locations. After this additional data is transformed and joined to the original data frame, a series of calculations were performed 


Because this project uses data sourced from .csv files, there were no actual connections made to any databases. As a showcase, I've included a script (database-export.py) based on the original pipeline which exports data from a hypothetical Teradata database and then exports additional data from a Microsoft SQL server database.

## Dashboard Overview
Though the data is different, all parts of this dashboard reflect the layout and functionality of the original.
