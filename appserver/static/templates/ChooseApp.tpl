<style>
	.wrapper-app-list {
		/*margin: 10px 0 10px 15px;*/
	    box-sizing: border-box;
	}
	.single-app {
		margin-bottom: 10px;
		padding: 10px;
		border: 1px solid black;
	    height: 100px;
	    box-sizing: border-box;
	}
	.single-app:hover {
		background-color: #d0cece;
		cursor: pointer;
	}
	.val-name {
		text-align: center;
		padding-left: 4px;
		margin-top:32px;
		font-size: 14px;
	}
	#get-archive-app {
		display: none;
	}
</style>
<h2>
	Выберите приложение для архивации:
</h4>
<div class="container">
	<div class="row">
		<%
			appsInfo.each(function(appInfo, idx) {
		%>
			<div class="span4">
				<div class="single-app" data-idx="<%= idx %>">
					<div class='val-name'><%= appInfo.get('name') %></div>
				</div>
			</div>
		<%
			});
		%>
	</div>
	<a href="" id="get-archive-app">Скачать</a>
</div>