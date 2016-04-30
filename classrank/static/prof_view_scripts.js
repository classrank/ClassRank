var semesterDropdown;
var courseDropdown;
var sectionDropdown;
var courses; //array of dicts with "year", "semester", "name", and "section" keys

function prof_js_init(prof_username)
{
    semesterDropdown = document.getElementById("SemesterDropdown");
    courseDropdown = document.getElementById("CourseDropdown");
    sectionDropdown = document.getElementById("SectionDropdown");

    var http = new XMLHttpRequest();

    alert("Opening http request");
    http.open("GET", "/api/professor/courses/?username=" + prof_username);
    http.onload = function (e) {
        if(http.readyState === 4)
        {
            if(http.status === 200)
            {
                alert("SUCCESS ? ");
                console.log(http.responseText);
                courses = JSON.parse(http.responseText);
                populateSemesterDropdown();
            }
            else
            {
                console.error(http.statusText);
            }
        }
    }

    http.onerror = function (e) {
        console.error(http.statusText);   
    }

    http.send();
}

function populateSemesterDropdown()
{
    var semesterList = [];

    //populate the first dropdown with the unique
    //year + semester values
    for (var i = 0; i < courses.length; i++)
    {
	var semesterStr = courses[i]["semester"] + " " + courses[i]["year"]

	// capitalize semester name
	semesterStr = semesterStr.charAt(0).toUpperCase() + semesterStr.slice(1);

	var unique = true;

	//certainly there is a better/faster way to do this
	//but I don't know js at all. Feel free to improve
	for (var j = 0; j < semesterList.length; j++)
	{
            if (semesterList[j] === semesterStr)
            {
		unique = false;
		break;
            }
	}

	if (unique)
	{
            semesterList.push(semesterStr)
	}
    }

    for(var i = 0; i < semesterList.length; i++)
    {
	var newOption = new Option(semesterList[i]);
	semesterDropdown.add(newOption);
    }
}

function clearCourseDropdown()
{
    while(courseDropdown.length > 1)
    {
	courseDropdown.remove(1);
    }

    courseDropdown.value = "Course"
}

function clearSectionDropdown()
{
    while(sectionDropdown.length > 1)
    {
	sectionDropdown.remove(1);
    }

    sectionDropdown.value = "Section"
}


/*
  |
  |  FILTERING FUNCTIONS
  |
*/

function semesterSelected()
{
    clearCourseDropdown();
    clearSectionDropdown();

    var selection = semesterDropdown.value.split(" ");
    var semester = selection[0];
    var semester = semester.charAt(0).toLowerCase() + semester.slice(1);
    var year = parseInt(selection[1]);

    var filteredCourses = [];

    for(var i = 0; i < courses.length; i++)
    {
	if(courses[i]["semester"] === semester && courses[i]["year"] == year)
	{
            var unique = true;

            for (var j = 0; j < filteredCourses.length; j++)
            {
		if (filteredCourses[j] === courses[i]["name"])
		{
		    unique = false;
		    break;
		}
            }

            if(unique)
            {
		filteredCourses.push(courses[i]["name"]);
            }
	}
    }

    for(var i = 0; i < filteredCourses.length; i++)
    {
	var courseOption = new Option(filteredCourses[i]);
	courseDropdown.add(courseOption);
    }
}

function courseSelected()
{
    clearSectionDropdown();

    var semesterSelection = semesterDropdown.value.split(" ");
    var semester = semesterSelection[0];
    var semester = semester.charAt(0).toLowerCase() + semester.slice(1);
    var year = parseInt(semesterSelection[1]);

    var course = courseDropdown.value;

    var filteredSections = [];

    for(var i = 0; i < courses.length; i++)
    {
	if(courses[i]["semester"] === semester && courses[i]["year"] == year && courses[i]["name"] === course)
	{
            //no need to check for uniqueness...
            //couse section + year + semester are unique by definition
            
            filteredSections.push(courses[i]["section"]);
	}
    }

    for(var i = 0; i < filteredSections.length; i++)
    {
	var sectionOption = new Option(filteredSections[i]);
	sectionDropdown.add(sectionOption);
    }
}

function sectionSelected()
{
    //course is completely selected.
    //this is where we can trigger the display of information
}
