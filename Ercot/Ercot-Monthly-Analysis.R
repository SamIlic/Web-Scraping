

#install.packages("xlsx")
#install.packages("readxl") # CRAN version
library(xlsx)
library(readxl)
require(car)
library(ggplot2)
cat("\014")  # clear console

# Set wordking directory so that we can read in the data file
setwd("/Users/YoungFreeesh/Visual Studio Code/_Python/Web Scraping/Ercot")

# read in data as a data frame
dfMASTER = read_excel("Test-Ercot-Scrape.xlsx", sheet = "Sheet1")
df052018 = read_excel("Test-Ercot-Scrape.xlsx", sheet = "05-2018")
df062018 = read_excel("Test-Ercot-Scrape.xlsx", sheet = "06-2018")

##### 05-2018
summary(df052018$HB_SOUTH)
summary(df052018$LZ_SOUTH)

plot.HB_SOUTH <- ggplot(df052018, aes(df052018$`Interval Ending`, df052018$HB_SOUTH)) #aes(X axis, Y axis)
plot.HB_SOUTH + geom_point() + labs(title = "HB_South Price vs Time of Day: 05-2018" , x = "Hour of Day", y = "HB_South Prices ($/MWh)")

plot.LZ_SOUTH <- ggplot(df052018, aes(df052018$`Interval Ending`, df052018$LZ_SOUTH)) #aes(X axis, Y axis)
plot.LZ_SOUTH + geom_point() + labs(title = "LZ_South Price vs Time of Day: 05-2018" , x = "Hour of Day", y = "LZ_South Prices ($/MWh)")

summary(df052018$`Interval Ending`[df052018$HB_SOUTH > 40]) # summary of outliers for time of day
summary(df052018$`Interval Ending`[df052018$LZ_SOUTH > 40]) # summary of outliers for time of day

##### 06-2018
summary(df062018$HB_SOUTH)
summary(df062018$LZ_SOUTH)

plot.HB_SOUTH <- ggplot(df062018, aes(df062018$`Interval Ending`, df062018$HB_SOUTH)) #aes(X axis, Y axis)
plot.HB_SOUTH + geom_point() + labs(title = "HB_South Price vs Time of Day: 06-2018" , x = "Hour of Day", y = "HB_South Prices ($/MWh)")

plot.LZ_SOUTH <- ggplot(df062018, aes(df062018$`Interval Ending`, df062018$LZ_SOUTH)) #aes(X axis, Y axis)
plot.LZ_SOUTH + geom_point() + labs(title = "LZ_South Price vs Time of Day: 06-2018" , x = "Hour of Day", y = "LZ_South Prices ($/MWh)")

summary(df062018$`Interval Ending`[df062018$HB_SOUTH > 40]) # summary of outliers for time of day
summary(df062018$`Interval Ending`[df062018$LZ_SOUTH > 40]) # summary of outliers for time of day



#plot.master_HB_SOUTH <- ggplot(dfMASTER, aes(dfMASTER$`Oper Day`, dfMASTER$HB_SOUTH)) #aes(X axis, Y axis)
#plot.master_HB_SOUTH + geom_point() + labs(title = "HB_South Price vs Day: 06-2018" , x = "Day", y = "HB_South Prices ($/MWh)") + theme(text = element_text(size=20), axis.text.x = element_text(angle=90, hjust=1)) 

#plot(dfMASTER$HB_SOUTH, main = "HB_South Prices: Everyday (so far)", ylab = "HB_South Prices ($/MWh)", xlab = "Every15 Min Price is Plotted")
#lines(dfMASTER$HB_SOUTH, y = NULL, type = "l")

outliers1 = df062018$`Interval Ending`[which(df062018$LZ_SOUTH > 40)]
outliers2 = df052018$`Interval Ending`[which(df052018$LZ_SOUTH > 40)]

OutlierTrend = function(outliers) {
  arr = c()
  tempCount = 0
  tempTime = 1
  for (time in 2:length(outliers)) {
    if (outliers[time] > outliers[time - 1]) {
      tempCount = tempCount + 1
    } else {
      #print(tempCount)
      arr = append(arr,tempCount)
      tempCount = 0
    }
  }
  arr
}

OutlierTrend(outliers1)
print(mean(OutlierTrend(outliers1)))
OutlierTrend(outliers2)
print(mean(OutlierTrend(outliers2)))

