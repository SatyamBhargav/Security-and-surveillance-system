const inputs = document.querySelectorAll(".input");


function addcl()
{
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl()
{
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach
(input => 
	{
		input.addEventListener("focus", addcl);
		input.addEventListener("blur", remcl);
	}
);

function check()
{
    var x = document.forms["myform"]["username"].value;
    var y = document.forms["myform"]["password"].value;
    if(x == "admin" && y == "admin")
    {
        alert("Login credential matched! Welcome")
        return true;
    }
    else
    {
        //alert("Wrong password. Please try again");
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Invalid Username or Password!'
          });
        return false;
    }
}

