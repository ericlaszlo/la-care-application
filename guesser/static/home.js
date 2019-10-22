var canvas, ctx, flag = false,
	  prevX = 0,
	  currX = 0,
	  prevY = 0,
	  currY = 0,
	  dot_flag = false;

var styleColor = "black",
	  brushSize = 20;

function init() {
	canvas = document.getElementById('canvas_area');
	ctx = canvas.getContext("2d");
	w = canvas.width;
  h = canvas.height;

	canvas.addEventListener("mousemove", function(e) {
		findxy('move', e)
	}, false);
	canvas.addEventListener("mousedown", function(e) {
		findxy('down', e)
	}, false);
	canvas.addEventListener("mouseup", function(e) {
		findxy('up', e)
	}, false);
	canvas.addEventListener("mouseout", function(e) {
		findxy('out', e)
	}, false);
}

function draw() {
	ctx.beginPath();
	ctx.moveTo(prevX, prevY);
	ctx.lineTo(currX, currY);
	ctx.strokeStyle = styleColor;
	ctx.lineWidth = brushSize;
	ctx.shadowBlur = 2;
	ctx.lineJoin = ctx.lineCap = 'round';
	ctx.stroke();
	ctx.closePath();
}

function erase() {
	ctx.clearRect(0, 0, w, h);
	predicted_digit.innerHTML = '?';
	predicted_score.innerHTML = '0.000';
}

function findxy(res, e) {
	if (res == 'down') {
		prevX = currX;
		prevY = currY;
		currX = e.clientX - canvas.offsetLeft;
		currY = e.clientY - canvas.offsetTop;

		flag = true;
		dot_flag = true;
		if (dot_flag) {
			ctx.beginPath();
			ctx.fillStyle = styleColor;
			ctx.fillRect(currX, currY, 2, 2);
			ctx.closePath();
			dot_flag = false;
		}
	}
	if (res == 'up' || res == 'out') {
		flag = false;
	}
	if (res == 'move') {
		if (flag) {
			prevX = currX;
			prevY = currY;
			currX = e.clientX - canvas.offsetLeft;
      currY = e.clientY - canvas.offsetTop;
			draw();
		}
	}
}

function SetBrushSize() {
	brushSize = document.getElementById("brush_select").value;
}
