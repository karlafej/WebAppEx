library(shiny)
library(httr)

# load helper functions
source("helpers.R")

# list ids in Microsoft Face API
list_id <- list(science = 4, movie = 5, porn = 2)

photo_number <- 1

shinyServer(function(input, output) {
  
  backto1 <- reactive({
    message("reset")
    if (input$face_url=="") return( )
    photo_number <<- 1
  })
  
  increase <- reactive({
    if ( input$nextButt == 0 ) return(  )
    message("nextbutton")
    photo_number <<- photo_number + 1
    # if photo_number > number of photos, let it be reseted to 1
    if (photo_number > length(faces())) photo_number <<- 1
  })
  
  faces <- reactive({
    # if image is loaded...
    req(input$face_url)
    message("faces")
    # ...register the image at Face API... 
    id = face_upload(input$face_url)
    # ...compare it to the database...
    face_similar(id, list_id[[input$imageset]])
  })  
  
  her <- reactive({
    # if image is loaded...
    req(input$face_url)
    increase()
    backto1()
    message("her")
    # ...and from the results, select the best one
    face_bestmatch(faces(), input$imageset, photo_number)
  })  
  
  output$hername <- renderUI({
    h1(her()$name)
  })
  
  output$herurl <- renderUI({
    a(img(alt=her()$url, src=her()$url, width="13%"),
      href=her()$link, target="_blank")
  })
  
  output$herconf <- renderUI({
    span(p("Confidence: ", as.character(round(her()$confidence*100)), 
      "%"), style="color:red")
  })

})
