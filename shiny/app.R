library(shiny)

# load our data 
data(mtcars)

# make cyl a factor
mtcars$cyl <- as.factor(mtcars$cyl)

# run our regression
fit <- lm(mpg ~ cyl + disp + qsec + am, data = mtcars)

preds <- function(fit, disp, qsec, cyl, am){
    # get the predicted MPG from new data
    mpg <- predict(object=fit, 
                   newdata = data.frame(
                       cyl=factor(cyl, levels=c('4', '6', '8')), 
                       disp=disp, 
                       qsec=qsec, 
                       am=am))
    
    # return as character string that can be easily rendered
    return(as.character(round(mpg, 2)))
}

app <- shinyApp(ui = fluidPage(title = 'Predicting MPG',
                # create inputs for each variable in the model 
                    sliderInput('disp', label = 'Displacement (in cubic inches)', 
                                min = floor(min(mtcars$disp)), 
                                max = ceiling(max(mtcars$disp)),
                                value = floor(mean(mtcars$disp))),
                    
                               
                    sliderInput('qsec', label='Quarter mile time',
                               min = floor(min(mtcars$qsec)), 
                                max = ceiling(max(mtcars$qsec)),
                                value = floor(mean(mtcars$qsec))),
                               
                    # this will return a character vector of length 1
                    # that will get converted into a factor
                    radioButtons('cyl', label='Number of cylinders',
                                choices = levels(mtcars$cyl),
                                inline=TRUE),
                               
                    # am is binary, 1/0, so we can coerse logical to integer   
                    checkboxInput('am', label='Has manual transmission'),
                               
                    # return our estimate
                    h3("Predicted MPG: ", textOutput('prediction'))),
                
                
               server = function(input, output){
                   # pass our inputs to our prediction function defined earlier
                   # and pass that result to the output
                   output$prediction <- renderText({
                        preds(fit= fit, 
                            disp = input$disp,
                            qsec = input$qsec,
                            cyl = input$cyl,
                            am = as.integer(input$am))
                   })
               })

# and run it
# runApp(app)


