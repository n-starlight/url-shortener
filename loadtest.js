import http from 'k6/http';
import {sleep,check} from 'k6';

//define http requests that you would like to test

export let options = {
    stages: [
        // { duration: '10s', target: 10 },  // Start with 10 users for 10 seconds
        // { duration: '10s', target: 50 },  // Ramp up to 50 users for 10 seconds
        // { duration: '20s', target: 60 }, 
        // { duration: '60s', target: 60},
        // { duration: '60s', target: 100 }, 
        { duration: '3m', target: 100 },
        { duration: '12m', target: 150 }, 
        // { duration: '10m', target: 200 }, 
        // { duration: '30s', target: 500 },
        // { duration: '30s', target: 1000 }, 
        { duration: '10s', target: 0 },   // Gradually ramp down to 0 users
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests should complete within 500ms
        http_req_failed: ['rate<0.05'],   // Failures should be below 5%
    },
    summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(50)', 'p(90)', 'p(95)', 'p(99)'],
};

// export let options = {
//     scenarios:{
//         smallLoad:{
//             executor : 'constant-vus',
//             vus:10, // To simulate 10 simultaneous requests 
//             duration:'10s' //each user will send requests for a duration of 10 seconds 
//         },
//     },
//     summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(50)', 'p(90)', 'p(95)', 'p(99)'], 
// };

const BASE_URL= 'http://127.0.0.1:8000' ;
const TEST_URL= "https://example.com" ;

export default function(){

    // post endpoint test

    let postPayload = JSON.stringify({url_link:TEST_URL}) //Javacript value to JSON string
    let postHeaders = {'Content-Type':'application/json'} ;
    let postres = http.post(`${BASE_URL}/shorten`,postPayload,{headers:postHeaders})
    // console.log(postres.json("short_url"))
    check(postres,{
        "response code was 200": (postres)=>postres.status==200,
        "short_url is returned": (postres)=>postres.json("short_url") !==undefined && postres.json("short_url") !==null 
        }
    )
    // || console.error("Request failed or database conn not available");

    // let short_code = postres.json("short_url");

    // get endpoint test

    // let short_code="c984d0" // to test get endpoint individually

    // let getres=http.get(`${BASE_URL}/redirect?short_code=${short_code}`,{redirects:0});
    // check(getres,{
    //     "response code was 307": (getres)=>getres.status===307,
    //     "redirection is correct" : (getres) =>getres.headers['Location']===TEST_URL
    // });

    sleep(1);

}