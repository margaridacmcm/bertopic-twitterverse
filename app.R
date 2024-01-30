library(shiny)
library(plotly)
library(readr)
library(stringr)
library(shinythemes)
library(plyr)
library(dplyr)
library(zoo)
library(shinytitle)

df <- read_csv('topic_data.csv', show_col_types = FALSE)
df$month <- as.POSIXct(as.yearmon(df$date, "%m-%Y"))

ui <- fluidPage(theme = shinytheme("superhero"),
                title = "117th Congress Tweet Topics",
                use_shiny_title(),
                titlePanel(h1("Congress 117th Tweet Topics", align="center",
                              style='padding: 30px')),
                fluidRow(
                  sidebarPanel(
                    div(style="display:inline-block",
                        selectizeInput("member", label=h4("Select Congress Member:"), 
                                       options = list(placeholder=' '),choices = sort(unique(df$member)), width = 250)),
                    
                    div(style="display:inline-block; margin-left: 20px",
                        selectizeInput("topic", label=h4("Select Topic:"), choices = sort(unique(df$topic_name)), width = 250)),
                    
                    width = 12,
                    style='text-align: center;')
                ),
                
                column(3,
                       div(style="text-align:center; padding-bottom: 0px", htmlOutput("title")),
                       div(style="text-align:center; color: #d3d3d3", htmlOutput("topics")),
                       div(style="text-align:center", imageOutput("image")),
                       
                       div(style="text-align:center", htmlOutput("color")),
                       div(style="text-align:center", htmlOutput("account")),
                       div(style="text-align:center", htmlOutput("totaltweets")),
                       div(style="text-align:center", htmlOutput("ranking"))
                ),
                
                column(9,
                       div(style="background-color: transparent;text-align:center", htmlOutput("tweets")),
                       div(style="text-align:center", htmlOutput("title1")),
                       div(style="background-color: transparent;", plotlyOutput("plot",
                                                                                height = '500px')),
                       div(style="text-align:center", htmlOutput("title2")),
                       div(style="background-color: transparent;", plotlyOutput("plot2",
                                                                                height = '500px'))
                       
                )
)


server <- function(input,output, session){
  observeEvent(input$member, {
    updateSelectizeInput(session,
                         inputId = "topic",
                         choices = c(df %>% filter(member == input$member) %>% 
                                       select(topic_name) %>% 
                                       unique() %>% 
                                       arrange(topic_name)))
  })
  
  
  output$title <- renderUI({
    h1(paste0(input$member))
  })
  
  output$image <- renderImage({
    list(
      src = file.path(paste0("images/", input$member,".jpg")),
      contentType = "image/jpeg",
      height = "100%"
    )
  }, deleteFile = FALSE)

  output$color <- renderUI({
    df_t <- subset(df, member %in% input$member)
    h4(paste0(df_t$party[1]))
  })
  
  output$account <- renderUI({
    df_t <- subset(df, member %in% input$member)
    c <- unique(df_t$handle)
    if (length(c) == 2) {
      c1 = unique(df_t$handle)[1]
      c2 = unique(df_t$handle)[2]
      h4(paste0("@",c1, ", @", c2))
    }
    else {
      c1 = unique(df_t$handle)[1]
      h4(paste0("@",c1))
    }
  })
  
  output$totaltweets <- renderUI({
    df_t <- subset(df, member %in% input$member & topic_name %in% input$topic)
    h4(paste0(dim(df_t)[1], " tweets on ", input$topic))
  })
  
  output$topics <- renderUI({
    df_t <- subset(df, member %in% input$member)
    t <- df_t %>% 
      group_by(topic_name) %>% 
      summarise(count_tweets = n()) %>%
      arrange(desc(count_tweets)) 
    
    tt <- as.data.frame(head(t))$topic_name
    if (dim(t)[1] == 1){h4(paste0(" ", tt[1]))}
    else if (dim(t)[1] == 2){h4(paste0(" ", tt[1], ", ", tt[2]))}
    else if (dim(t)[1] > 2){h4(paste0(" ", tt[1], ", ", tt[2], ", ", tt[3]))}
  })
  
  output$ranking <- renderUI({
    df_t <- subset(df, topic_name == input$topic)
    df_tt <- df_t %>% 
      group_by(member) %>% 
      summarise(count_tweets = n()) %>%
      arrange(desc(count_tweets)) 
    
    if (input$member %in% df_tt$member) {
      aux <- which(df_tt$member == input$member)
      h4(paste0("#", aux, " out of ", dim(df_tt)[1]))
      }
  })
  
  output$tweets <- renderUI({
    df_t <- subset(df, member %in% input$member & topic_name %in% input$topic)
    if (dim(df_t)[1] == 0) {h3(paste0(input$member, " didn't tweet about ", input$topic))}
    else {
      i <- sample.int(dim(df_t)[1], 1)
      em(h3(paste0(df_t$tweet[i])))
    }    
  })
  
  output$title1 <- renderUI({
    df_t <- subset(df, member %in% input$member & topic_name %in% input$topic)
    if (dim(df_t)[1] != 0) {
    h2(paste0("Tweeting frequency on ", input$topic))
    }
  })
  
  output$title2 <- renderUI({
    df_t <- subset(df, member %in% input$member & topic_name %in% input$topic)
    if (dim(df_t)[1] != 0) {
    h2(paste0("Ranking position on ", input$topic))
    }
  })
  
  output$plot <- renderPlotly({
    #all members tweet counts
    df_t <- subset(df, topic_name == input$topic) %>% ungroup()
    df_tt <- df_t %>% 
      group_by(month, topic_name) %>% 
      summarise(count_tweets = n()) %>%
      arrange(month)
    
    #selected member tweet counts
    df_t2 <- subset(df_t, member == input$member) %>% ungroup()
    df_tt2 <- df_t2 %>% 
      group_by(month, topic_name) %>% 
      summarise(count_tweets = n()) %>%
      arrange(month)
    if (dim(df_tt2)[1] != 0){
      #now plot!
      plot_ly()  %>% 
        layout(paper_bgcolor='rgba(0, 0, 0, 0)',
               plot_bgcolor  = "rgba(0, 0, 0, 0)",
               xaxis = list(tickfont = list(size = 15), tickformat="%b %y", dtick='M1'),
               yaxis = list(tickfont = list(size = 20), gridcolor = '#5A5A5A'),
               font = list(color = '#D3D3D3')) %>%
               #title = list(text = paste0("Tweeting frequency on ", input$topic),font = list(size=25))) %>% 
        add_trace(y=df_tt$count_tweets, name="Congress Tweets", x=df_tt$month,
                mode='linesmarkers', type='bar',marker =list(color = '#00008B')) %>% 
        add_trace(y=df_tt2$count_tweets, name=paste0(input$member, " Tweets"), x=df_tt2$month, type='scatter',mode='linesmarkers', 
                  line =list(color = '#8b0000'), marker =list(color = '#8b0000'))
    }
  })
  
  output$plot2 <- renderPlotly({
    df_t <- subset(df, topic_name == input$topic)
    df_aux <- subset(df_t, member == input$member)
    df_tt <- df_t %>% 
      group_by(member) %>% 
      summarise(count_tweets = n()) %>%
      arrange(desc(count_tweets))
    
    if (dim(df_aux)[1] != 0) {
      plot_ly()  %>%
        layout(paper_bgcolor='rgba(0, 0, 0, 0)',
               plot_bgcolor  = "rgba(10, 0, 0, 0)",
               xaxis = list(tickfont = list(size = 15), categoryorder = 'max descending', showticklabels =FALSE),
               yaxis = list(tickfont = list(size = 20), gridcolor = '#5A5A5A'),
               font = list(color = '#D3D3D3'),
               showlegend = FALSE) %>%

        add_trace(y=df_tt$count_tweets, x=df_tt$member, type='bar', 
                  colors = "Set1",color= df_tt$member == input$member) 
    }
  })

}

shinyApp(ui = ui, server = server)





