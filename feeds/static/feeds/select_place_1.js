// 마커를 클릭하면 장소명을 표출할 인포윈도우 입니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.76424769662378, 128.89930503464964), // 지도의 중심좌표
        level: 5 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption); 
let sb
const hid = document.getElementById('hid')
const hid2 = document.getElementById('hid2')
const markers = []
// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places(); 
function onKeyPress(event) {
    if(event.keyCode ===13){
        sKey = document.getElementById('test').value
        ps.keywordSearch(sKey, placesSearchCB);
        document.getElementById('test').value = null;
    }
}
function onSubmit(event){
    sKey = document.getElementById('test').value
    ps.keywordSearch(sKey, placesSearchCB);
    document.getElementById('test').value = null;
}
// 키워드로 장소를 검색합니다
function placesSearchCB (data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        var bounds = new kakao.maps.LatLngBounds();

        for (var i=0; i<data.length; i++) {
            displayMarker();    
            bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
        }       

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
        map.setBounds(bounds);
    } 
}

// 지도에 마커를 표시하는 함수입니다
function displayMarker() {
    var startSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/red_b.png', // 출발 마커이미지의 주소입니다    
    startSize = new kakao.maps.Size(50, 45), // 출발 마커이미지의 크기입니다 
    startOption = { 
        offset: new kakao.maps.Point(15, 43) // 출발 마커이미지에서 마커의 좌표에 일치시킬 좌표를 설정합니다 (기본값은 이미지의 가운데 아래입니다)
    };

    var startImage = new kakao.maps.MarkerImage(startSrc, startSize, startOption);
    var marker = new kakao.maps.Marker({ 
        position: map.getCenter(),
        image: startImage
    }); 

    // 지도에 마커를 표시합니다
    marker.setMap(map);

    kakao.maps.event.addListener(map, 'click', function(mouseEvent) {        
        var latlng = mouseEvent.latLng; 
        // 마커 위치를 클릭한 위치로 옮깁니다
        marker.setPosition(latlng);
        console.log(latlng)
        lat = latlng.getLat()
        lng = latlng.getLng()
        sb = latlng
        var iwContent = '<div style="padding:5px;">이 장소를 <button onclick="hi()">등록</button></div>'; // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
        // 인포윈도우를 생성합니다
        var infowindow = new kakao.maps.InfoWindow({
            content : iwContent
        });
        kakao.maps.event.addListener(marker, 'mouseover', function() {
            infowindow.open(map, marker);
        });
    })
}
function hi(){
    console.log(marker)
    var startSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/red_b.png', // 출발 마커이미지의 주소입니다    
    startSize = new kakao.maps.Size(50, 45), // 출발 마커이미지의 크기입니다 
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
    hid.value += sb.Ga+"/"
    hid2.value += sb.Ha+"/"
}