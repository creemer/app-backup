<style>
  #progress {
    background: #b8b8b8;
    width: 100%;
    margin-top: 9px;
    -webkit-border-radius: 10px;
    -moz-border-radius: 10px;
    border-radius: 10px;
  }
  .button-wrapper {
    margin-bottom: 20px;
  }
  .bar {
    height: 18px;
    background: green;
    -webkit-border-radius: 10px;
    -moz-border-radius: 10px;
    border-radius: 10px;
  }
  #fileupload {
    display: none;
  }
  #upload-btn {
    display: none;
  }
  .form-wrapper {
    width: 500px;
  }
  .vert-offset {
    height: 10px;
  }
  .form-field-label {
    text-align: right;
    padding-right: 4px;
    padding-top: 5px;
  }
</style>
<h2>
  Загрузить приложение:
</h2>

<input id="fileupload" type="file" name="app" data-url="<%= url %>" multiple="true"/>
<div class="form-wrapper">
  <div class="row-fluid">
      <div class="span4">
        <div class="form-field-label">
          <button class="btn" id="upload-handler">Выбрать приложение</button>
        </div>
      </div>
      <div class="span8">
        <div id="progress">
          <div class="bar" style="width: 0%;"></div>
        </div>
        <div class="file-name">
          <span id="file-name"></span>
        </div>       
      </div>
  </div>
  <div class="vert-offset"></div>
  <div class="row-fluid">
      <div class="span4">
        <div class="form-field-label">
          Место назначения:
        </div>
      </div>
      <div class="span8">
        <div>
          <select id="dist-select">
            <%
              _.each(linkData, function(singleDestination) {
            %>
              <option value="<%= singleDestination.val %>">
                <%= singleDestination.name %>
              </option>
            <%
              });
            %>
          </select>
        </div>
      </div>
  </div>
  <div class="row-fluid">
    <div class="span4">
      <div class="form-field-label">
        <button id="deploy-btn" class="btn btn-primary">Загрузить</button>
      </div>
    </div>
  </div>
</div>
