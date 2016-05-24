# twitter_finder
Find Trends(#) &amp; Most Popular person/company(@) in a time period on Twitter


##how it works:
###Input-
    - Range of time period (from - to)
    - input.txt (4 text files): list of screen name (or username) of twitter's profile
###Output-
  	- First it will print Trends(#hashtags) & Most Popular person/company(@mentions) and their frequencies in descending order for all screen names from input file
  	- Then, it will print Trends(#hashtags) & Most Popular person/company(@mentions) for whole list of profiles and their frequencies in descending order by taking intersection with all individual profile's #hashtags & @mentions, respectively in a time period
    - At last, it will print Trends(#hashtags) & Most Popular person/company(@mentions) and generate the bar graphs by taking the intersection of all four text input file's hashtags and mentions as a cross groups matching and print the results.

#####Note: It will only print frequencies which is more than one.
