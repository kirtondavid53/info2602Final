/*
const server = "http://127.0.0.1:5000";

async function getData(){
    try{
      let response = await fetch(`${server}/getreacts`);//1. Send http request and get response
      let result = await response.json();//2. Get data from response
      setSelect(result);// 3. Do something with the data
      console.log(result);
   }catch(e){
       console.log(e);//catch and log any errors
   }
 }

 function setSelect(data){
    for(let rec of data){
        document.getElementById("mySelect").value = "dislike";
    }
 }

getData();

*/