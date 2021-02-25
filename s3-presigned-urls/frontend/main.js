Dropzone.autoDiscover = false;
Dropzone.prototype.defaultOptions.dictDefaultMessage = 'Drop files here or tap this box to generate a color scheme. Files are Limited to 1MB and are deleted regularly.'
var myDropzone = new Dropzone("div#mydropzone", { url: S3_URL});

var urlData = {}
fetch(API_URL_BASE + "generate")
  .then(response => response.json())
  .then(data => 
  {
    urlData = data
  });

myDropzone.on('sending', async function(file, xhr, formData){
    var i;
    for (const f in urlData){
        formData.append(f, urlData[f]);
    }
});

myDropzone.on("complete", function(file){
  myDropzone.removeFile(file);
  document.getElementById('uploadyourimage').innerHTML = 'Generating your color scheme... Give it a minute!';
  document.getElementById('mydropzone').style.display = 'none';
  document.getElementById('hr-divider').style.display = 'none';
  updatePage();
});

function updatePage() {
  setTimeout(() => {
    document.getElementById("schemeImg").src = S3_URL + urlData['key'];
    fetch(API_URL_BASE + 'colors/' + urlData['key'])
    .then(response => response.json())
    .then(data => 
    {
      var parsedData = JSON.parse(data['rgb']) 
      document.body.style.backgroundColor = parsedData['dominant'];
      document.getElementById('thebodytoo').style.backgroundColor = parsedData['dominant'];
      let i = 0;
      var palette = parsedData['palette']
      while (i < palette.length) { 
        i++;
        document.getElementById("color" + i).style.backgroundColor = palette[i-1];
        document.getElementById("color" + i + 'rgb').innerHTML = palette[i-1];
      }
    });
    document.getElementById('uploadyourimage').style.display = 'none';
  }, 15000)
}
