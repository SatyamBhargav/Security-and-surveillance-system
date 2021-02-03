let {PythonShell} = require('python-shell')
 
function motion_detection()
{
    let options = {
        //pythonPath: 'C:/Users/msoft/AppData/Local/Programs/Python/Python39',
        scriptPath: 'D:/Project/system/engine/Motion_detection'
      };
       
      PythonShell.run('Plotting.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
      });
}

function Bio_scan()
{
    let options = {
        //pythonPath: 'C:/Users/msoft/AppData/Local/Programs/Python/Python39',
        scriptPath: 'D:/Project/system/engine/Biometric_scanner'
      };
       
      PythonShell.run('Biometric_Scanner.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
      });
      
}

function add_face()
{
   
  var name = document.getElementById("name").value
  let options = {
      //pythonPath: 'C:/Users/msoft/AppData/Local/Programs/Python/Python39',
      scriptPath: 'D:/Project/system/engine/Biometric_scanner',
      args : ["on",name]
    };
    /*  
    PythonShell.run('addface.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      console.log('results: %j', results);
    });*/
    var face = new PythonShell("addface.py", options);

    face.end(function(err, code, message) {
      Swal.fire(
        'Face added!',
        'We can now recognize your face',
        'success'
      )
      /*swal("Face added!","We can now recognize your face","success")*/
    })
}






/*
let {PythonShell} = require('python-shell')
var path = require("path")


function motion_detection()
{
    document.getElementById("motionD").value = "Hang on.."

    var options = {
        scriptPath : path.join(__dirname, 'D:/testing phase/system/engine/')
        //pythonPath : 'C:/Users/msoft/AppData/Local/Programs/Python/Python38'
    }

    let face = new PythonShell("motion_detection.py", options);

    face.end(function(err, code, message) {
        document.getElementById("motionD").value = "Detection faces";
    })

}*/

