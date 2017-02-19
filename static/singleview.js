var method = 'socketio'; // 'ajax'

// COMMON

$(document).ready(function() {
	load_link_triggers();
});

function load_link_triggers() {
	$('a[href^="##"]').each(function() {
		$(this).on('click', function(e) {
			e.preventDefault();
			$page = $(this).attr('href').replace('##', '');
			if ($page[0] === '/') {
				$page = $page.substr(1);
			}
			changePage($page);
		});
	});
}

// SOCKETIO

if (method === 'socketio') {
	new_socket = function(namespace='') {
		namespace = '/' + namespace.substr(namespace.indexOf('/') + 1);
		return io.connect('http://' + document.domain + ':' + location.port + namespace, {'force new connection': true});
	}

	var sockets = {
		page: new_socket('page')
	};

	sockets.page.on('page', function(data) {
		$('#singleview-content').html(atob(data)).show();
		$('a[href^="##"]').unbind('click');
		load_link_triggers();
	});
}

// COMMON

function currentPath() {
	var path = window.location.pathname;
	if (path[0] === '/') {
		path = path.substr(1);
	}
	return path;
}

// ~ COMMON ~

function changePage(path, backforth=false) {
	if ((currentPath() === path && backforth === true) || currentPath() !== path) {
		$('#singleview-content').hide();
		if (method === 'socketio') {
			emitPage(path);
		} else if (method === 'ajax') {
			postPage(path);
		}
	}
	if (backforth === false) {
		var current_url = window.location.protocol + "//" + window.location.host + '/' + path;
		window.history.pushState({path:current_url},'',current_url);
	}
}

window.onpopstate = function(event) {
	var url = window.location.protocol + "//" + window.location.host + '/';
	if(event.state !== null) {
		var page = event.state.path.slice(event.state.path.indexOf(url) + url.length);
		changePage(page, true);
	} else {
		changePage('', true);
	}
}

// SOCKETIO

function emitPage(path) {
	sockets.page.emit('get page', {"page": path});
}

// AJAX

function postPage(path) {
	$.post(window.location.protocol + "//" + window.location.host + '/page', {page: path}).done(function(data) {
		$('#singleview-content').html(atob(data)).show();
		$('a[href^="##"]').unbind('click');
		load_link_triggers();
	});
}