let lats = document.getElementById('lats').attributes[1].nodeValue
let longs = document.getElementById('longs').attributes[1].nodeValue
//lats = lats.split('/')
//longs = longs.split('/')
const latList = lats.split('/')
const longList = longs.split('/')
latList.pop()
longList.pop()

const latAvg = average(latList)
const longAvg = average(longList)
console.log(longAvg,latAvg)
function average(array){
    var sum = 0.0;
    for (var i = 0; i < array.length; i++){
        sum += parseFloat(array[i]);
    }
    return sum / array.length;
}

var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
    mapOption = { 
        center: new kakao.maps.LatLng(longAvg, latAvg), // 지도의 중심좌표
        level: 7 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
const positions = []
for(let i=0; i<latList.length; i++){
    console.log(longList[i],latList[i])
    positions.push(
        {   
            latlng: new kakao.maps.LatLng(parseFloat(longList[i]),parseFloat(latList[i]))
        }
    )
}

// 마커 이미지의 이미지 주소입니다
var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
    
for (var i = 0; i < positions.length; i ++) {
    
    // 마커 이미지의 이미지 크기 입니다
    var imageSize = new kakao.maps.Size(24, 35); 
    
    // 마커 이미지를 생성합니다    
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
    
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        map: map, // 마커를 표시할 지도
        position: positions[i].latlng, // 마커를 표시할 위치
        image : markerImage // 마커 이미지 
    });
}