document.addEventListener('DOMContentLoaded', function () {

    $.get('http://localhost:5000/api/restaurants', function(data){
        console.log(data)
        data.forEach(function (array){
            element = array[0]
            $('.stack').append('<li><h1>' + element.name + '</h1></li>')
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
        var stack = gajus.Swing.Stack(config);
    
        [].forEach.call(document.querySelectorAll('.stack li'), function (targetElement) {
            stack.createCard(targetElement);
            targetElement.classList.add('in-deck');
            
            stack.getCard(targetElement).on('throwout', function(e){
                console.log(e.target.innerText || e.target.textContent, 'has been thrown out of the stack to the', e.throwDirection, 'direction.');
                e.target.classList.remove('in-deck');
            })
            stack.getCard(targetElement).on('throwin', function (e) {
                console.log(e.target.innerText || e.target.textContent, 'has been thrown into the stack from the', e.throwDirection, 'direction.');
        
                e.target.classList.add('in-deck');
            });
        });
    })
    

  


    $('.stack li').on('click', function(){
        if ($(this).hasClass('in-deck')){
            console.log('fscren')
            $(this).toggleClass('fullscreen')
        }
    
    })

});

