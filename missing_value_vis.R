get_missing_patterns <- function(dataset) {
  # get missing patterns from a dataset
  missing_patterns <- data.frame(is.na(dataset)) %>%
    group_by_all() %>%
    count(name = "count", sort = TRUE) %>%
    ungroup()
  return(missing_patterns)
}

count_missing_col <- function(dataset) {
  test <- sort(colSums(is.na(dataset)),decreasing = TRUE)
  df <- data.frame(test, names(test))
  colnames(df) <- c('num rows missing','variable')
  return(df)
}

percent_missing_col <- function(dataset) {
  testp <- sort(colSums(is.na(dataset)),decreasing = TRUE)
  dfp <- data.frame(testp, names(testp))
  colnames(dfp) <- c('num rows missing','variable')
  df <- dfp %>% mutate(totalrow = nrow(dataset)) %>% mutate(`% rows missing` = `num rows missing` / totalrow * 100)
  return(df)
}

sideplotpart1_count <- function(dataset){
  ## get barplot from dataset counting missing value of each feature
  df = count_missing_col(dataset)
  sp1c <- ggplot(data = df,aes(x = factor(variable, levels = df$variable), y = `num rows missing`)) +
    geom_histogram(stat='identity',fill='grey50') + 
    scale_x_discrete('')  + 
    theme(panel.grid.major.x = element_blank(),
          axis.text.x = element_text(angle = 75, vjust = 0.5, hjust=0.5))
  return(sp1c)
}

sideplotpart1_percent <- function(dataset){
  ## get barplot from dataset computing missing percentage of each feature
  df = percent_missing_col(dataset)
  sp1p <- ggplot(data = df, aes(x = factor(variable, df$variable), y = `% rows missing`)) +
    geom_histogram(stat='identity',fill='grey50') + 
    scale_x_discrete('')  + 
    scale_y_continuous(limits=c(0,100))  +
    theme(panel.grid.major.x = element_blank(),
          axis.text.x = element_text(angle = 75, vjust = 0.5, hjust=0.5))
  return(sp1p)
  
}

get_complete_pattern <- function(patterns) {
  indicator <- (rowSums(patterns[1:length(patterns) - 1]) == 0)
  return (row.names(patterns)[indicator])
}

sideplotpart2_count <- function(dataset){
  ## get barplot count each pattern's occurence
  ## highlight the complete pattern
  library(dplyr)
  missing_patterns <- get_missing_patterns(dataset)
  dfmissing <- data.frame(row.names(missing_patterns),missing_patterns$count)
  colnames(dfmissing) <- c('patterns','row count')
  
  complete_pattern = get_complete_pattern(missing_patterns)
  dfmissingupdate <- dfmissing %>% mutate(newfalse = ifelse(patterns == complete_pattern,1,0))
  sp2c <- ggplot(data = dfmissingupdate,
                 aes(x = fct_rev(reorder(patterns,-`row count`)), 
                     y = `row count`,fill = ifelse(newfalse ==  "1", "Highlighted", "Normal") )) + 
    geom_histogram(stat='identity') + 
    scale_x_discrete('')  + 
    scale_fill_manual(values=c("red","grey50")) +
    theme(legend.position = "none", axis.title.y = element_blank(),panel.grid.major.y = element_blank()) +
    coord_flip()
  return(sp2c)
}


sideplotpart2_percent <- function(dataset){
  ## get barplot computing percentage of each pattern
  ## highlight the complete pattern
  missing_patterns <- get_missing_patterns(dataset)
  dfmissing <- data.frame(row.names(missing_patterns), missing_patterns$count)
  colnames(dfmissing) <- c('patterns','row count')
  
  complete_pattern = get_complete_pattern(missing_patterns)
  dfmissingupdate <- dfmissing %>%
    mutate(newfalse = ifelse(patterns == complete_pattern,1,0)) %>%
    mutate(totalrow = nrow(dataset)) %>%
    mutate(`% rows` = `row count`/ totalrow * 100)
  sp2p <- ggplot(data = dfmissingupdate,
                 aes(x = fct_rev(reorder(patterns, -`% rows`)), y = `% rows`,fill = ifelse(newfalse ==  "1","Highlighted", "Normal") )) + 
    geom_histogram(stat='identity') + 
    scale_x_discrete('')  + 
    scale_y_continuous(limits=c(0,100)) +
    scale_fill_manual(values=c("red","grey50")) +
    theme(legend.position = "none", axis.title.y = element_blank(),panel.grid.major.y = element_blank()) +
    coord_flip()
  return(sp2p)
}

missing_plot <- function(missing_pattern, complete_row, feature_order){
  library(ggplot2)
  library(gghighlight)
  library(reshape2)
  # given a pattern plot not including
  melted_pattern <- melt(as.matrix(missing_pattern[1:length(missing_pattern) - 1]))
  colnames(melted_pattern) <- c("pattern", "feature", "missing")
  melted_pattern$pattern = as.character(melted_pattern$pattern)
  melted_pattern$color_type = as.integer(melted_pattern$missing)
  melted_pattern$color_type[melted_pattern$pattern == as.character(complete_row)] = 2
  melted_pattern$color_type <- as.character(melted_pattern$color_type)
  melted_pattern$feature <- factor(melted_pattern$feature, levels=feature_order)
  
  p <-  ggplot(melted_pattern, aes(feature, factor(pattern, levels = row.names(missing_pattern)))) +
    geom_tile(aes(fill = color_type), color = 'white', show.legend = FALSE) +
    scale_fill_manual(values = c("lightblue", "grey", "orange")) +
    scale_y_discrete(limits = rev) +
    labs(x="feature",  y="missing pattern") +
    annotate(geom="text", x=length(missing_pattern) / 2, y = nrow(missing_pattern[0]) + 1 - as.integer(complete_row), label="Complete Pattern", color="black")+
    theme(axis.text.x = element_text(angle = 75, vjust = 0.5, hjust=0.5))
  return(p)
}

# paste three pictures together
paste <- function(sidegraph1, mainplot, sidegraph2){
  output <- sidegraph1 + plot_spacer() + mainplot + sidegraph2 + plot_layout(widths = c(4, 1), heights = c(1, 4))
  return(output)
}

# main function
main_missing_plot <- function(dataset, percent) {
  if (percent) {
    feat_ord <- percent_missing_col(dataset)$variable
    side1 <- sideplotpart1_percent(dataset)
    side2 <- sideplotpart2_percent(dataset)
  } else {
    feat_ord <- count_missing_col(dataset)$variable
    side1 <- sideplotpart1_count(dataset)
    side2 <- sideplotpart2_count(dataset)
  }
  pattern <- get_missing_patterns(dataset)
  complete_pattern <- get_complete_pattern(pattern)
  mainplot <- missing_plot(pattern, complete_pattern, feat_ord)
  return (paste(side1, mainplot, side2))
}

