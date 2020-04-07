/*
This is empty on purpose! Your code to build the resume will go here.
 */
var work = {
	"jobs" : [
	{
		"employer" : "XJAU",
	    "title" : "讲师",
	    "location" : "新疆",
	    "dates" : "2003",
	    "description" : "这是一个好又不好的工作！"
	},
	{ "employer" : "MyHome",
	    "title" : "家长",
	    "location" : "新疆",
	    "dates" : "1979",
	    "description" : "这是40年的工作！"

	}
	  
	]
};
 
var projects = {
	"projects" : [{

		"title" : "aaaprojcet",
		"dates" : "2003",
		"description" : "This is a aaaprojcet.",
		"images" : [
			 "images/fry.jpg","http://www.baidu.com"
		]
	},{

		"title" : "bbbprojcet",
		"dates" : "2012",
		"description" : "This is a bbbprojcet.",
		"images" : ["images/fry.jpg","http://www.baidu.com"
		]
	}
	]

};

var bio = {
  "name" : "xielan",
  "role" : "Teacher",
  "welcomeMessage" : "Hello,This is me !",
  "contacts" :　{
    "mobile" : "13999266079",
    "email" : "xielan@xjau.edu.cn",
    "weibo" : "xhl112",
    "WeiChat" : "xhl@302",
    "location" :  "xinjiang"
  },
  "skills" : [
    "发牢骚","看书"
  ],
  "bioPic": "images/fry.jpg"

};
var education = {
	"schools": [{
		"name": "小学",
		"location" : "青河县",
		"degree" : "小学毕业",
		"dates" : "1991",
		"url" : "http://www.qinghe.com",
		"major" : ["数学","语文"]
	},{
		"name": "中学",
		"location" : "哈巴河县",
		"degree" : "中学毕业",
		"dates" : "1998",
		"url" : "http://www.habahe.com",
		"major" : ["物理","化学"]

	},{
		"name": "大学",
		"location" : "乌鲁木齐",
		"degree" : "管理学学士",
		"dates" : "1991",
		"url" : "http://www.xjau.edu.cn",
		"major" : ["C语言","Java语言"]
	}
	],
	"onlineCourses" : [
		{
			"title" : "Logic",
			"school" : "英国",
			"dates"  : "2015",
			"url" : "http://www.coursera.org"
		},
		{
			"title" : "Pyton",
			"school" : "美国莱斯大学",
			"dates"  : "2014",
			"url" : "http://www.coursera.org"
		}
	]
};

var displayWork = function(){
HTMLheaderName = HTMLheaderName.replace("%data%",bio.name);
$("#header").append(HTMLheaderName);

if ( bio.skills.length > 0 ){
 	$("#header").append(HTMLskillsStart);

 	var formattedSkill = HTMLskills.replace("%data%",bio.skills[0]);
 	$("#skills").append(formattedSkill);
 	formattedSkill = HTMLskills.replace("%data%",bio.skills[1]);
 	$("#skills").append(formattedSkill);
};

for( key in work.jobs){
	$("#workExperience").append(HTMLworkStart);

	var formattedEmployer = HTMLworkEmployer.replace("%data%",
		work.jobs[key].employer);
	var formattedTitle = HTMLworkTitle.replace("%data%",
		work.jobs[key].title);
	var formattedEmployerTitle = formattedEmployer + formattedTitle;
	$(".work-entry:last").append(formattedEmployerTitle);

	var formattedDate = HTMLworkDates.replace("%data%",
		work.jobs[key].dates);
	$(".work-entry:last").append(formattedDate);
	
	var formattedLocation = HTMLworkLocation.replace("%data%",
		work.jobs[key].location);
	$(".work-entry:last").append(formattedLocation);
	
	var formattedDescription = HTMLworkDescription.replace("%data%",
		work.jobs[key].description);
	$(".work-entry:last").append(formattedDescription);
}
}



function inName(name){
	var newName = name.split(" ");
	var n1 = newName[0].charAt(0).toUpperCase() + newName[0].slice(1);
	var n2 = newName[1].toUpperCase();
	newName = n1 + n2;
	return newName; 
}

console.log(inName("xie lan"));

$("#main").append(internationalizeButton);