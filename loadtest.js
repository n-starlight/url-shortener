import http from 'k6/http';
import {sleep,check} from 'k6';

//define http requests that you would like to test

export let options = {
    scenarios:{
        smallLoad:{
            executor : 'constant-vus',
            vus:10, // To simulate 10 simultaneous requests 
            duration:'10s' //each user will send requests for a duration of 10 seconds 
        },
    },
};

const BASE_URL= 'http://127.0.0.1:8000' ;
const TEST_URL= "https://www.w3schools.com/html/default.asp" ;

export default function(){

    // post endpoint test

    let postPayload = JSON.stringify({url_link:TEST_URL}) //Javacript value to JSON string
    let postHeaders = {'Content-Type':'application/json'} ;
    let postres = http.post(`${BASE_URL}/shorten`,postPayload,{headers:postHeaders})
    check(postres,{
        "response code was 200": (postres)=>postres.status==200,
        "short_url is returned": (postres)=>(postres.body).length >=1
        }
    );

    let short_code = JSON.parse(postres.body).short_url.split("/").pop();

    // get endpoint test

    let getres=http.get(`${BASE_URL}/redirect?short_code=${short_code}`);
    check(getres,{
        "response code was 200": (getres)=>getres.status==307 || getres.status == 302,
        "redirection is correct" : (getres) =>getres.headers['Location']==TEST_URL
    });

    sleep(1);

}