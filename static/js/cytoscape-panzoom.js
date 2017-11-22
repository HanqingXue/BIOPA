/*!
Copyright (c) The Cytoscape Consortium

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
(function(){var register=function(cytoscape,$){if(!cytoscape||!$){return}$.fn.cyPanzoom=$.fn.cytoscapePanzoom=function(options){panzoom.apply(this,[options,cytoscape,$]);return this};cytoscape("core","panzoom",function(options){panzoom.apply(this,[options,cytoscape,$]);return this})};var defaults={zoomFactor:0.05,zoomDelay:45,minZoom:0.1,maxZoom:10,fitPadding:50,panSpeed:10,panDistance:10,panDragAreaSize:75,panMinPercentSpeed:0.25,panInactiveArea:8,panIndicatorMinOpacity:0.5,zoomOnly:false,fitSelector:undefined,animateOnFit:function(){return false},fitAnimationDuration:1000,sliderHandleIcon:"fa fa-minus",zoomInIcon:"fa fa-plus",zoomOutIcon:"fa fa-minus",resetIcon:"fa fa-expand"};var panzoom=function(params,cytoscape,$){var cyRef=this;var options=$.extend(true,{},defaults,params);var fn=params;var functions={destroy:function(){var $this=$(cyRef.container());var $pz=$this.find(".cy-panzoom");$pz.data("winbdgs").forEach(function(l){$(window).unbind(l.evt,l.fn)});$pz.data("cybdgs").forEach(function(l){cyRef.off(l.evt,l.fn)});$pz.remove()},init:function(){var browserIsMobile="ontouchstart" in window;return $(cyRef.container()).each(function(){var $container=$(this);$container.cytoscape=cytoscape;var winbdgs=[];var $win=$(window);var windowBind=function(evt,fn){winbdgs.push({evt:evt,fn:fn});$win.bind(evt,fn)};var windowUnbind=function(evt,fn){for(var i=0;i<winbdgs.length;i++){var l=winbdgs[i];if(l.evt===evt&&l.fn===fn){winbdgs.splice(i,1);break}}$win.unbind(evt,fn)};var cybdgs=[];var cyOn=function(evt,fn){cybdgs.push({evt:evt,fn:fn});cyRef.on(evt,fn)};var cyOff=function(evt,fn){for(var i=0;i<cybdgs.length;i++){var l=cybdgs[i];if(l.evt===evt&&l.fn===fn){cybdgs.splice(i,1);break}}cyRef.off(evt,fn)};var $panzoom=$('<div class="cy-panzoom"></div>');$container.prepend($panzoom);$panzoom.css("position","absolute");$panzoom.data("winbdgs",winbdgs);$panzoom.data("cybdgs",cybdgs);if(options.zoomOnly){$panzoom.addClass("cy-panzoom-zoom-only")}var $zoomIn=$('<div class="cy-panzoom-zoom-in cy-panzoom-zoom-button"><span class="icon '+options.zoomInIcon+'"></span></div>');$panzoom.append($zoomIn);var $zoomOut=$('<div class="cy-panzoom-zoom-out cy-panzoom-zoom-button"><span class="icon '+options.zoomOutIcon+'"></span></div>');$panzoom.append($zoomOut);var $reset=$('<div class="cy-panzoom-reset cy-panzoom-zoom-button"><span class="icon '+options.resetIcon+'"></span></div>');$panzoom.append($reset);var $slider=$('<div class="cy-panzoom-slider"></div>');$panzoom.append($slider);$slider.append('<div class="cy-panzoom-slider-background"></div>');var $sliderHandle=$('<div class="cy-panzoom-slider-handle"><span class="icon '+options.sliderHandleIcon+'"></span></div>');$slider.append($sliderHandle);var $noZoomTick=$('<div class="cy-panzoom-no-zoom-tick"></div>');$slider.append($noZoomTick);var $panner=$('<div class="cy-panzoom-panner"></div>');$panzoom.append($panner);var $pHandle=$('<div class="cy-panzoom-panner-handle"></div>');$panner.append($pHandle);var $pUp=$('<div class="cy-panzoom-pan-up cy-panzoom-pan-button"></div>');var $pDown=$('<div class="cy-panzoom-pan-down cy-panzoom-pan-button"></div>');var $pLeft=$('<div class="cy-panzoom-pan-left cy-panzoom-pan-button"></div>');var $pRight=$('<div class="cy-panzoom-pan-right cy-panzoom-pan-button"></div>');$panner.append($pUp).append($pDown).append($pLeft).append($pRight);var $pIndicator=$('<div class="cy-panzoom-pan-indicator"></div>');$panner.append($pIndicator);function handle2pan(e){var v={x:e.originalEvent.pageX-$panner.offset().left-$panner.width()/2,y:e.originalEvent.pageY-$panner.offset().top-$panner.height()/2};var r=options.panDragAreaSize;var d=Math.sqrt(v.x*v.x+v.y*v.y);var percent=Math.min(d/r,1);if(d<options.panInactiveArea){return{x:NaN,y:NaN}}v={x:v.x/d,y:v.y/d};percent=Math.max(options.panMinPercentSpeed,percent);var vnorm={x:-1*v.x*(percent*options.panDistance),y:-1*v.y*(percent*options.panDistance)};return vnorm}function donePanning(){clearInterval(panInterval);
windowUnbind("mousemove",handler);$pIndicator.hide()}function positionIndicator(pan){var v=pan;var d=Math.sqrt(v.x*v.x+v.y*v.y);var vnorm={x:-1*v.x/d,y:-1*v.y/d};var w=$panner.width();var h=$panner.height();var percent=d/options.panDistance;var opacity=Math.max(options.panIndicatorMinOpacity,percent);var color=255-Math.round(opacity*255);$pIndicator.show().css({left:w/2*vnorm.x+w/2,top:h/2*vnorm.y+h/2,background:"rgb("+color+", "+color+", "+color+")"})}function calculateZoomCenterPoint(){var pan=cyRef.pan();var zoom=cyRef.zoom();zx=$container.width()/2;zy=$container.height()/2}var zooming=false;function startZooming(){zooming=true;calculateZoomCenterPoint()}function endZooming(){zooming=false}var zx,zy;function zoomTo(level){if(!zooming){calculateZoomCenterPoint()}cyRef.zoom({level:level,renderedPosition:{x:zx,y:zy}})}var panInterval;var handler=function(e){e.stopPropagation();e.preventDefault();clearInterval(panInterval);var pan=handle2pan(e);if(isNaN(pan.x)||isNaN(pan.y)){$pIndicator.hide();return}positionIndicator(pan);panInterval=setInterval(function(){cyRef.panBy(pan)},options.panSpeed)};$pHandle.bind("mousedown",function(e){handler(e);windowBind("mousemove",handler)});$pHandle.bind("mouseup",function(){donePanning()});windowBind("mouseup blur",function(){donePanning()});$slider.bind("mousedown",function(){return false});var sliderVal;var sliding=false;var sliderPadding=2;function setSliderFromMouse(evt,handleOffset){if(handleOffset===undefined){handleOffset=0}var padding=sliderPadding;var min=0+padding;var max=$slider.height()-$sliderHandle.height()-2*padding;var top=evt.pageY-$slider.offset().top-handleOffset;if(top<min){top=min}if(top>max){top=max}var percent=1-(top-min)/(max-min);$sliderHandle.css("top",top);var zmin=options.minZoom;var zmax=options.maxZoom;var x=Math.log(zmin)/Math.log(zmax);var p=(1-x)*percent+x;var z=Math.pow(zmax,p);if(z<zmin){z=zmin}else{if(z>zmax){z=zmax}}zoomTo(z)}var sliderMdownHandler,sliderMmoveHandler;$sliderHandle.bind("mousedown",sliderMdownHandler=function(mdEvt){var handleOffset=mdEvt.target===$sliderHandle[0]?mdEvt.offsetY:0;sliding=true;startZooming();$sliderHandle.addClass("active");var lastMove=0;windowBind("mousemove",sliderMmoveHandler=function(mmEvt){var now=+new Date;if(now>lastMove+10){lastMove=now}else{return false}setSliderFromMouse(mmEvt,handleOffset);return false});windowBind("mouseup",function(){windowUnbind("mousemove",sliderMmoveHandler);sliding=false;$sliderHandle.removeClass("active");endZooming()});return false});$slider.bind("mousedown",function(e){if(e.target!==$sliderHandle[0]){sliderMdownHandler(e);setSliderFromMouse(e)}});function positionSliderFromZoom(){var z=cyRef.zoom();var zmin=options.minZoom;var zmax=options.maxZoom;var x=Math.log(zmin)/Math.log(zmax);var p=Math.log(z)/Math.log(zmax);var percent=1-(p-x)/(1-x);var min=sliderPadding;var max=$slider.height()-$sliderHandle.height()-2*sliderPadding;var top=percent*(max-min);if(top<min){top=min}if(top>max){top=max}$sliderHandle.css("top",top)}positionSliderFromZoom();cyOn("zoom",function(){if(!sliding){positionSliderFromZoom()}});(function(){var z=1;var zmin=options.minZoom;var zmax=options.maxZoom;var x=Math.log(zmin)/Math.log(zmax);var p=Math.log(z)/Math.log(zmax);var percent=1-(p-x)/(1-x);if(percent>1||percent<0){$noZoomTick.hide();return}var min=sliderPadding;var max=$slider.height()-$sliderHandle.height()-2*sliderPadding;var top=percent*(max-min);if(top<min){top=min}if(top>max){top=max}$noZoomTick.css("top",top)})();function bindButton($button,factor){var zoomInterval;$button.bind("mousedown",function(e){e.preventDefault();e.stopPropagation();if(e.button!=0){return}var doZoom=function(){var zoom=cyRef.zoom();var lvl=cyRef.zoom()*factor;if(lvl<options.minZoom){lvl=options.minZoom}if(lvl>options.maxZoom){lvl=options.maxZoom}if((lvl==options.maxZoom&&zoom==options.maxZoom)||(lvl==options.minZoom&&zoom==options.minZoom)){return}zoomTo(lvl)};startZooming();doZoom();zoomInterval=setInterval(doZoom,options.zoomDelay);return false});windowBind("mouseup blur",function(){clearInterval(zoomInterval);endZooming()})}bindButton($zoomIn,(1+options.zoomFactor));bindButton($zoomOut,(1-options.zoomFactor));$reset.bind("mousedown",function(e){if(e.button!=0){return}var elesToFit=options.fitSelector?cyRef.elements(options.fitSelector):cyRef.elements();if(elesToFit.size()===0){cyRef.reset()}else{var animateOnFit=typeof options.animateOnFit==="function"?options.animateOnFit.call():options.animateOnFit;if(animateOnFit){cyRef.animate({fit:{eles:elesToFit,padding:options.fitPadding}},{duration:options.fitAnimationDuration})}else{cyRef.fit(elesToFit,options.fitPadding)}}return false})})}};if(functions[fn]){return functions[fn].apply(this,Array.prototype.slice.call(arguments,1))}else{if(typeof fn=="object"||!fn){return functions.init.apply(this,arguments)}else{$.error("No such function `"+fn+"` for jquery.cytoscapePanzoom")}}return $(this)};if(typeof module!=="undefined"&&module.exports){module.exports=function(cytoscape,jquery){register(cytoscape,jquery||require("jquery"))
}}else{if(typeof define!=="undefined"&&define.amd){define("cytoscape-panzoom",function(){return register})}}if(typeof cytoscape!=="undefined"&&typeof jQuery!=="undefined"){register(cytoscape,jQuery)}})();