# Pended Claims Queue Dashboard
## Background
During my tenure at Commonwealth Care Alliance, I was tasked with creating a data dashboard to summarize metrics

Medical claims can pend for a variety of reasons. While CCA had multiple different queues for pended claims, for simplicity's sake, this project outline only focuses on the primary pending claims queue.

## ETL Pipeline Overview

On a regularly scheduled basis, a script I wrote extracted pending claims data from CCA's claims management systems database. This data was loaded into a pandas dataframe for transformation. After being formatted, certain fields were used to query CCA's provider database to pull additional data about rendering providers and service locations. After this additional data is transformed and joined to the original data frame, a 

## Dashboard Overview
While all parts of this dashboard reflect the layout of the original project, for obvious reasons the original data couldn't be used. This PowerBI dashboard sources synthetic Medicare claims data provided by CMS. You can find this dataset at:
https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-20

To simulate 
