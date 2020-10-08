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
let infowindow
const markers = []
let markerList = []
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
hello()
function hello(){
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
    // 지도에 마커를 표시합니다
    marker.setMap(map);
    markerList.push(marker)
    kakao.maps.event.addListener(map, 'click', function(mouseEvent) {        
        var latlng = mouseEvent.latLng; 
        // 마커 위치를 클릭한 위치로 옮깁니다
        marker.setPosition(latlng);
        lat = latlng.getLat()
        lng = latlng.getLng()
        sb = latlng
        var iwContent = '<div style="padding:5px;">이 장소를 <button onclick="hi()">등록</button></div>'; // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
        // 인포윈도우를 생성합니다
        infowindow = new kakao.maps.InfoWindow({
            content : iwContent
        });
        kakao.maps.event.addListener(marker, 'mouseover', function() {
            infowindow.open(map, marker);
        });       
    })
}

}



function hi(){
    infowindow.close()
    var startSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png', // 출발 마커이미지의 주소입니다    
    startSize = new kakao.maps.Size(24, 35)
    startOption = { 
        offset: new kakao.maps.Point(15, 43) // 출발 마커이미지에서 마커의 좌표에 일치시킬 좌표를 설정합니다 (기본값은 이미지의 가운데 아래입니다)
    };
    var startImage = new kakao.maps.MarkerImage(startSrc, startSize, startOption);
    var marker = new kakao.maps.Marker({ 
        position: sb,
        image: startImage,
    }); 
    // 지도에 마커를 표시합니다
    markers.push([sb.Ga,sb.Ha])
    marker.setMap(map);
    markerList.push(marker)
    hid.value += sb.Ga+"/"
    hid2.value += sb.Ha+"/"
}

function setMarkers(map) {
    console.log(markerList,markerList.length)
    for (var i = 0; i < markerList.length; i++) {
        markerList[i].setMap(map);
        infowindow.close() 
    }    
    markerList=[]
    hello()
    console.log(positions)
}

// "마커 감추기" 버튼을 클릭하면 호출되어 배열에 추가된 마커를 지도에서 삭제하는 함수입니다
function hideMarkers() {
    setMarkers(null);   
}
