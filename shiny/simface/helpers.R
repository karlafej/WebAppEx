# Face API key - replace this with your actual key
faceKEY = "************************************"

# pornhub info
infos = list(porn = read.csv("pornhub_list.tsv", sep="\t", as.is=TRUE),
             movie = read.csv("imdb_list.tsv", sep="\t", as.is=TRUE),
             science = read.csv("science_list.tsv", sep="\t", as.is=TRUE))

# upload image to Microsoft FACE, return FACE api id
face_upload <- function(img.url) {
  faceURL = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=age,gender,smile,facialHair"
  
  #stopifnot(!http_error(GET(img.url)))
  
  mybody = list(url = img.url)
  
  faceResponse = POST(
    url = faceURL, 
    content_type('application/json'), add_headers(.headers = c('Ocp-Apim-Subscription-Key' = faceKEY)),
    body = mybody,
    encode = 'json'
  )
  
  stopifnot(faceResponse$status == 200)
  
  content(faceResponse)[[1]][[1]]
}  

# take FACE api id and find all images that are similar
face_similar <- function(image.id, list.id) {
  simURL = "https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars"
  mybody2 = list(faceId = image.id, faceListId = list.id, mode = "matchFace")
  
  simResponse = POST(
    url = simURL, 
    content_type('application/json'), add_headers(.headers = c('Ocp-Apim-Subscription-Key' = faceKEY)),
    body = mybody2,
    encode = 'json'
  )
  
  stopifnot(simResponse$status_code == 200)
  
  content(simResponse)
}

# extract information for the best fit
face_bestmatch <- function(res, setname, k=1) {
  
  info <- infos[[setname]]
  
  idx <- which(info$faceId == res[[k]]$persistedFaceId)
  stopifnot(length(idx) == 1)
  list(name = info$name[idx],
       url = info$url[idx],
       link = info$link[idx],
       confidence = res[[k]]$confidence)
}
