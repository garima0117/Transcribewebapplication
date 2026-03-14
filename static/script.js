const fileInput = document.getElementById("audioFile")
const preview = document.getElementById("audioPreview")
const analyzeBtn = document.getElementById("analyzeBtn")

const loader = document.getElementById("loader")

const transcription = document.getElementById("transcription")
const sentimentBadge = document.getElementById("sentimentBadge")

fileInput.onchange = () => {

const file = fileInput.files[0]

if(file){
preview.src = URL.createObjectURL(file)
}

}


analyzeBtn.onclick = async () => {

const file = fileInput.files[0]

if(!file){
alert("Upload audio first")
return
}

const formData = new FormData()

formData.append("audio", file)

loader.style.display = "block"

const response = await fetch("/analyze",{

method:"POST",
body:formData

})

const data = await response.json()

loader.style.display = "none"

transcription.innerText = data.transcription

sentimentBadge.innerText = data.sentiment + " ("+data.score+")"

if(data.sentiment==="POSITIVE"){
sentimentBadge.style.background="green"
}

else{
sentimentBadge.style.background="red"
}

}