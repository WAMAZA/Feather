function loadMore(loadMoreBtn, currentItem, boxes, type){
   // check if the loading button should be displayed or not

   if(currentItem >= boxes.length){
      loadMoreBtn.style.display = 'none';
   }

   // show more publication when the load more btn has been clicked
   loadMoreBtn.onclick = () =>{
      let acc = 6 // accumulateur
      if (currentItem+acc <= boxes.length){
         for (var i = currentItem; i < currentItem + acc; i++) {
            if(type === "image"){
               boxes[i].style.display = 'inline-block';
            } else {
               boxes[i].style.display = 'flex';
            }
         }
      } else{
         acc = boxes.length - currentItem
         for (var i = currentItem; i < currentItem + acc; i++) {
            if(type === "image"){
               boxes[i].style.display = 'inline-block';
            } else {
               boxes[i].style.display = 'flex';
            }
         }
      }

      currentItem += acc;

      if(currentItem >= boxes.length){
         loadMoreBtn.style.display = 'none';
      }
   }
}
function countElem(field){
   let result = 0
   for (let i = 0; i < field.length; ++i){
      let getStyle = getComputedStyle(field[i]).getPropertyValue("display")
      if(getStyle !== "none" || getStyle === "flex"){
         result++
      }
   }
   return result
}

// accueil
let loadMoreBtnA = document.querySelector('#load-more');
let currentItemA = countElem(document.querySelectorAll('.recent-product .product'))
let boxesA = [...document.querySelectorAll('.recent-product .product')];

// bibliotheque
let loadMoreBtnB = document.querySelector('#load-more');
let currentItemB = countElem(document.querySelectorAll('.all-product .product'))

let boxesB = [...document.querySelectorAll('.all-product .product')];

// espace membre
let loadMoreBtnEM = document.querySelector('#load-more-em');
let currentItemEM = countElem(document.querySelectorAll('#myPub .pub-group'))

let boxesEM = [...document.querySelectorAll('.pub-content .pub-group')];

// espace membre like
let loadMoreBtnEmLike = document.querySelector('#load-more-em-like');
let currentItemEmLike = countElem(document.querySelectorAll('#mesLikes .pub-group'))
let boxesEmLike = [...document.querySelectorAll('.mesLikes .pub-group')];

// espace membre comment
let loadMoreBtnEmCom = document.querySelector('#load-more-em-com');
let currentItemEmCom = countElem(document.querySelectorAll('#mesComments .avis-box'))
let boxesEmCom = [...document.querySelectorAll('.mesComments .avis-box')];
console.log(currentItemEmCom)

if (document.querySelector(".recent-product")){
   loadMore(loadMoreBtnA, currentItemA, boxesA, 'image')
} else if (document.querySelector(".all-product")){
   loadMore(loadMoreBtnB, currentItemB, boxesB, 'image')
} else{
   if (loadMoreBtnEM){
      loadMore(loadMoreBtnEM, currentItemEM, boxesEM, 'produit')
   }
   if (loadMoreBtnEmLike){
      loadMore(loadMoreBtnEmLike, currentItemEmLike, boxesEmLike, 'produit')
   }
   if (loadMoreBtnEmCom){
      loadMore(loadMoreBtnEmCom, currentItemEmCom, boxesEmCom, 'produit')
   }
}

