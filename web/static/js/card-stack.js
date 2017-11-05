var stack

document.addEventListener('DOMContentLoaded', function () {

    $.get('http://localhost:5000/api/restaurants', function(data){
        console.log(data)
        data.forEach(function (array){
            element = array[0]
            var html = `
                <li id="`+ element.id + `">
                <div id="basic-info">
                    <img src="` + element.image_url +`" id="image1">
                    <h2 id="name">` + element.name + `</h2>
                    <h4 id="price">Price: ` + element.price +`</h4>
                    <h4 id="rate">Popularity: ` + element.popularity + ` </h4>
                    <h4 id="distance">` + (element.distance * 0.000621371).toPrecision(3) +` mi away</h4>
                </div>
                <div id="desc">
                <img src="` + element.image_url +`" id="image1">
                    <p id="name2">Name of the Resterarunt</p>
                    <p id="price2">Price: ` + element.price +`</p>
                    <p id="rate2">Popularity: ` + element.popularity +`</p>
                    <p id="distance2">0.9 mi away</p>
                    <p id="description_id2">Description:</p>
                    <p id="description2">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum
                    </p>
                </div>
            </li>
            `
            $('.stack').append(html)
            
        })
        var config = 
        {
            throwOutConfidence: function (offset, element) {
                // console.log(offset)
                // console.log(element.offsetWidth)
                var res = 0
                if (Math.abs(offset) / element.offsetWidth >= 0.4)
                    res = 1
                return res
            },
            throwOutDistance: function(){
                return 2000;
            }
        };
        stack = gajus.Swing.Stack(config);
    
        [].forEach.call(document.querySelectorAll('.stack li'), function (targetElement) {
            stack.createCard(targetElement);
            targetElement.classList.add('in-deck');
            
            stack.getCard(targetElement).on('throwout', function(e){
                swiped( (e.throwDirection == gajus.Swing.Card.DIRECTION_RIGHT) ? 1 : -1, $(targetElement).attr('id'))
                e.target.classList.remove('in-deck');
            })
            stack.getCard(targetElement).on('throwin', function (e) {
                e.target.classList.add('in-deck');
            });
        });
    })

    $('.stack li').click(function(){
            console.log('clicked')
            var x = document.getElementById('desc')
            var y = document.getElementById('basic-info')
            // var x = $("#desc")[0]
            // var y = $("#basic-info")[0]
                if (x.style.display === "none")
                 {
                    y.style.display = "none";
                    x.style.display = "block"; 
                } 
                else {
                    x.style.display = "none";
                    y.style.display = "block";
                }   
        })   

   // $('.stack li').on('click', function(){
   //      if ($(this).hasClass('in-deck')){
   //          $("#basic-info").hide();
   //          $("#desc").show();
   //      }
    
   //  })



    $('#reject').on('click', function(){
        var cards = document.querySelectorAll('.in-deck')
        var card = stack.getCard(cards[cards.length - 1])
        $(cards[cards.length - 1]).toggleClass('slow-animate')
        card.throwOut(gajus.Swing.Card.DIRECTION_LEFT, (Math.random() * 200 - 100))
    })
    $('#accept').on('click', function(){
        var cards = document.querySelectorAll('.in-deck')
        var card = stack.getCard(cards[cards.length - 1])
        $(cards[cards.length - 1]).toggleClass('slow-animate')
        card.throwOut(gajus.Swing.Card.DIRECTION_RIGHT, (Math.random() * 200 - 100))
    })
});

function swiped(like, id){
    $.post( "http://localhost:5000/api/restaurants/like", {'id' : id, 'like' : like })
}

