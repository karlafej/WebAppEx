
library(shiny)

shinyUI(fluidPage(

  fluidRow(
    column(12, 
           br(), br(),
           textInput("face_url", "Photo URL:", value="", width="95%")
#          submitButton("Submit", icon("search")), br(), br()
           )
  ),

  fluidRow(
    column(12,
           radioButtons("imageset", "Find your lookalike among:",
                        c("Scientists" = "science",
                          "Actors and Actresses" = "movie",
                          "Pornstars" = "porn"))
    )
  ),
  
  fluidRow(
    column(12, htmlOutput("hername"), align="center")
  ),
  
  fluidRow(
    column(12, htmlOutput("herurl"), align="center")
  ),
  
  fluidRow(
    column(12, htmlOutput("herconf"), align="center")
  ),
  
  conditionalPanel( condition = "input.face_url != ''",
    fluidRow(
      column(12, actionButton(inputId="nextButt", label=" Don't like it? Try again!", icon = icon("refresh")), align="center")
    )
  )
))
