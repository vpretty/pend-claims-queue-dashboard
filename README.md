# Pended Claims Queue Dashboard
This is an example ETL pipeline and PowerBI dashboard based on an actual project I completed during my tenure at Commonwealth Care Alliance during the fall of 2024. To abide with relevant NDAs, certain aspects of this project have been changed from the original.

This project uses synthetic Medicare claims data provided by CMS. You can find this dataset at:
https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-20

## Background
Commonwealth Care Alliance is a healthcare services organization which provides care delivery and health plans for Medicare and Medicaid recipients in the New England area. During my tenure there, I was tasked with creating a data dashboard to report metrics surrounding pending medical claims.

Medical claims can pend for a variety of reasons. This can range from incomplete provider or address data to data errors, such as the date of service being prior to the effective date of the location. While CCA had multiple different queues for pended claims, for simplicity's sake, this project outline only focuses on the primary pending claims queue.

## ETL Pipeline
On a regularly scheduled basis, a pipeline I wrote extracted pending claims data from CCA's claims management systems database. This data was loaded into a pandas dataframe for transformation. After being formatted, certain fields were used to query CCA's provider database to pull additional data about rendering providers and service locations. After this additional data was transformed and joined to the original data frame, a series of calculations were performed to determine the following metrics:

- Total Claims in Pending Queue.
- Total Dollar Amount of Pending Claims. 
- Total Unique Practitioners.
- Total Unique Provider Groups.
- Total Unique Facilities.
- Total Claims Cleared by Date.
- Aging Claims by Age Group. Age groups are as follows: 0-9 days, 10-20 days, 21-25 days, 26-30 days, <=30 days, 31-44 days, 45-60 days, 61-90 days, >90 days, and >30 days.
- Top 10, 20, and 30 Claims by Age.
- Aging Claims by Pending Category. Pending category was determined by the presence of certain phrases in claims comments. The pending categories are as follows: missing practitioner, missing group, missing agreement, entity category, DOS prior to effective date, address, and misc.

You can find the pipeline used to generate these calculations in calc_totals.py.

To simulate data exported from a pending claims queue, I added a number of fields to the synthetic Medicare claims dataset. You can find the script used to generate this data in cms_generation.py. The following fields were added:
- Rendering Provider First Name and Last Name. These names were randomly assigned to included providers by NPI and were pulled from the CMS.gov National Downloadable file of clinicians. This dataset can be found here: https://data.cms.gov/provider-data/dataset/mj5m-pzi6
- Service Location Address. Address 1, City, State, and Zip were added at the same time as rendering provider first name and last name, and were also pulled from the National Downloadable file of clinicians. In the original project, 
- Facility ID. These were also assigned at the same time as rendering provider first and last name and were pulled from the National Downloadable file of clinicians.
- Clear Date. The date the claim "left" the queue, aka the date the claim was resolved. 15% of the claims in the dataset were randomly selected to have a clear date. This clear date was taken from column CLM_THRU_DT.
- Claim Age. Applicable only to claims which weren't given a clear date. "Current Date" was chosen to be one day after the max date of the synthetic Medicare Claims dataset column "CLM_THRU_DT". Claim ages were then calculated using this chosen date.
- Comments. Within CCA's claim's management software, claim adjudicators are able to leave comments to signal why a claim was placed in the pending queue. While this is a free-text field, I was able to extract a list of common phrases used in claims comments. These phrases were randomly assigned to included claims.
- Report Date. The date the data was "pulled". This field is generated in calc_totals.py and is used in visualizations in the Power BI dashboard.


## Dashboard Overview
Though the data is different, all parts of this dashboard reflect the layout and functionality of the original. You can find this dashboard in Pending Claims Dashboard.pbix.

For the purposes of demonstrating visuals, some of the data generated in calc_totals.py was duplicated with sequential dates to mimic a week's worth of data.

The tabs included in the dashboard are as follows:
- Summary. A summary of key metrics with a card displaying total claims in the pending queue.
- Top pending claims by age. Pending claims ordered by age, with filters for top 10, top 20, and top 30 claims.
- Pending claims. All pending claims with age category.
- Pending claims by category. A count of unique claims by the category of their associated comment.
- Cleared claims. All cleared claims.
- Total groups. Total unique groups by group name.
- Total facilities. Total unique facilities by address.
- Total individuals. Total unique individual practitioners by NPI.
- Total claims left. Total claims cleared from queue per day.
- Total claims. Total claims in pending queue per day.
- Total dollars. Total cost claims in pending queue.
