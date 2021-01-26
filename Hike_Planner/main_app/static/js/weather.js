$(document).ready(function(){
    //get a location from the park selection
    function getWeather(){
        var long =  "-121.7043885";
        var lat =  "46.86075416";
        var API_KEY = 'd36ad86fcc0091b23f6132b4b6cc00e7'
        // let baseURL = `https://api.openweathermap.org/data/2.5/onecall?lat=${lat}&lon=${long}&units=imperial&appid=${API_KEY}`;

        $.get(baseURL, function(res) {
            console.log(res)
            let data = res.current;
            let temp = Math.floor(data.temp)
            let condition = data.weather[0].description

            $('#temp-main').html(`${temp}°`);
            $('#condition').html(condition);
        })
    }
    getWeather()
    //end doc ready
})