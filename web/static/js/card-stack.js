var stack

document.addEventListener('DOMContentLoaded', function () {

    $.get('http://localhost:5000/api/restaurants', function(data){
        console.log(data)
        data.forEach(function (array){
            element = array[0]
            $('.stack').append('<li id="' + element.id + '"><h1>' + element.name + '</h1><h2>'+ element.popularity + '</h2></li>')
            
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

