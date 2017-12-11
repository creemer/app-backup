<style>
	.overlay {
		position: absolute;
		top: 0;
		left: 0;
		z-index: 9000;
		background-color: rgba(0, 0, 0, 0.6);
		width: 100%;
		height: 100%;
	}
	.popup-body {
		margin-bottom: 10px;
	    -webkit-border-radius: 10px;
	    -moz-border-radius: 10px;
	    border-radius: 10px;
		margin: 100px auto;
		width: 200px;
		height: 200px;
		background-color: rgb(225, 225, 225);
	}
	.inside-wrapper {
		padding-top: 80px;
		padding-bottom: 20px;
		text-align: center;
	}
	.text-wrapper {
		font-size: 20px;
	}
</style>
<div class="overlay">
	<div class="popup-body">
		<div class="inside-wrapper">
			<div class="text-wrapper">
				<%= text %>
			</div>
		</div>
	</div>
</div>