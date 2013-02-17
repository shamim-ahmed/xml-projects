<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
                xmlns:pl="http://purl.org/rss/1.0/"
                version="2.0">
  <xsl:output method="html" />

  <xsl:template match="/">
    <html>
    <head>
      <title>Weather Forecast</title>
      <link rel="stylesheet" type="text/css" href="resources/css/style.css"/>
      <link rel="stylesheet" type="text/css" href="resources/css/tablesorter.css"/>
      <script type="text/javascript" src="resources/js/jquery-1.7.2.min.js"></script>
      <script type="text/javascript" src="resources/js/jquery.tablesorter.min.js"></script>  
      <script type="text/javascript" src="resources/js/custom.js"></script> 
    </head>
    <body> 
      <div id="fullpage">
        <div id="content">
          <!-- process the first file (Melbourne)-->
          <div>
            <xsl:apply-templates select="/product/forecast" />
          </div>
          
          <!-- process the second file (precise forecasts for Victorian cities) -->
          <div>
            <xsl:apply-templates select="document('IDV10580.xml')/product"/>
          </div> 
          
          <!-- process the third file (interstate cities)-->
          <div>
            <h2>Interstate Cities Forecast</h2>
            <table class="tablesorter forecasttable">
              <thead>
                <tr><th class="location">City</th><th class="forecast">Forecast</th><th>Min</th><th>Max</th></tr>
              </thead>
              <tbody>
                <xsl:apply-templates select="document('IDV17300.xml')/product/forecast/area">
                  <xsl:sort select="@description"/>
                </xsl:apply-templates>
              </tbody>
            </table>
          </div>    
          
          <!-- process the fourth file (events) -->
          <div class="events">
            <h2>Cultural Events</h2>
            <table class="tablesorter eventtable">
              <thead>
                <tr><th>Title</th><th>Link</th><th>Description</th></tr>
              </thead>
              <tbody>
                <!-- we show only the first three events -->
                <xsl:apply-templates select="document('rss_today.xml')/rdf:RDF/pl:item[position() &gt;= 1 and position() &lt;= 3]">
                  <xsl:sort select="pl:title"/>
                </xsl:apply-templates>
              </tbody>
            </table>           
          </div>
      </div>
      </div>
    </body>
    </html>
  </xsl:template>
 
  <!-- templates to process the first file --> 
  <xsl:template match="forecast">     
    <xsl:variable name="regionCode" select="area[@type='region']/@aac"/>
    <xsl:variable name="metroAreaCode" select="area[@parent-aac=$regionCode]/@aac"/>
    <xsl:variable name="metroAreaName" select="area[@parent-aac=$regionCode]/@description"/>
    <xsl:variable name="cityAreaCode" select="area[@parent-aac=$metroAreaCode and @description=$metroAreaName]/@aac"/>
    
    <h2><xsl:value-of select="$metroAreaName"/> Metropolitan Area Forecast</h2>
        
    <xsl:for-each select="area[@aac=$metroAreaCode]/forecast-period">
      <xsl:variable name="timestamp" select="@start-time-local"/>
      
      <xsl:variable name="dayOfWeek">
        <xsl:call-template name="getDayOfWeek">
          <xsl:with-param name="dateTime" select="$timestamp"/>
        </xsl:call-template>
      </xsl:variable>
      
      <xsl:if test="$dayOfWeek = 'Saturday' or $dayOfWeek = 'Sunday' or $dayOfWeek = 'Monday' or $dayOfWeek = 'Tuesday' or $dayOfWeek = 'Wednesday'"> 
        <div class="weekday-weather-info">
  	      <h3>Forecast for <xsl:value-of select="$dayOfWeek"/></h3>
  	      
  	      <xsl:variable name="cityForecast" select="/product/forecast/area[@aac=$cityAreaCode]/forecast-period[@start-time-local=$timestamp]"/>   
          <div class="container">
            <!-- display forecast for the metropolitan area -->
            <div><xsl:value-of select="text[@type='forecast']/text()"/></div> 
            
            <!-- display forecast for the city -->
            <div class="city-forecast">
              <div><span class="info-label">City : </span><xsl:value-of select="$cityForecast/text[@type='precis']/text()"/></div> 
                    
              <div class="city-container">         
                <div class="city-forecast-image">            
                  <xsl:call-template name="showWeatherIcon">
                    <xsl:with-param name="imageCode" select="$cityForecast/element[@type='forecast_icon_code']/text()"/>
                    <xsl:with-param name="iconType">big</xsl:with-param>
                  </xsl:call-template>
                </div>
                <div class="city-forecast-temp">
                  Min <span class="min"><xsl:value-of select="$cityForecast/element[@type='air_temperature_minimum']/text()"/></span><br/>
                  Max <span class="max"><xsl:value-of select="$cityForecast/element[@type='air_temperature_maximum']/text()"/></span>
                </div>
                <div class="full"> </div>      
              </div>    
            </div>
          </div>
        </div>
      </xsl:if>
    </xsl:for-each>        
  </xsl:template>
  
  <!-- templates to process the second file -->
  <xsl:template match="product">
    <h2>Precise Forecasts for Victorian Cities and Towns</h2>
    
    <xsl:variable name="dayOfWeek">
      <xsl:call-template name="getDayOfWeek">
        <xsl:with-param name="dateTime" select="amoc/validity-bgn-time-local"/>
      </xsl:call-template>
    </xsl:variable>
    
    <h3>Forecast for <xsl:value-of select="$dayOfWeek"/></h3>      
       
    <xsl:variable name="regionCode" select="forecast/area[@type='region']/@aac"/>
    <xsl:variable name="regionName" select="forecast/area[@type='region']/@description"/>
    
    <!-- iterate over the top-level areas, each of which results in a table in output -->
    <xsl:for-each select="forecast/area[@parent-aac=$regionCode]">
      <xsl:sort select="@description"/>
      
      <h4><xsl:value-of select="@description"/></h4>
      <xsl:variable name="areaCode" select="@aac"/>     
      
      <table class="tablesorter forecasttable"> 
        <thead>
          <tr><th class="location">Location</th><th class="forecast">Forecast</th><th>Min</th><th>Max</th></tr>
        </thead>
        <tbody>
          <!-- iterate over the areas within top-level areas, each of which appear as a row in a table -->
          <xsl:for-each select="/product/forecast/area[@parent-aac=$areaCode]">
            <xsl:sort select="@description"/>
            <tr>
              <td class="name location"><a target="_blank"><xsl:attribute name="href">/resources/static/map.html?location=<xsl:value-of select="@description"/>&amp;state=<xsl:value-of select="$regionName"/></xsl:attribute><xsl:value-of select="@description"/></a></td>
              <td class="forecast">
                 <xsl:call-template name="showWeatherIcon">
                   <xsl:with-param name="imageCode" select="forecast-period/element[@type='forecast_icon_code']/text()"/>
                   <xsl:with-param name="iconType">small</xsl:with-param>
                 </xsl:call-template>
                 <span class="message"><xsl:value-of select="forecast-period/text[@type='precis']/text()"/></span>
              </td>
              <td class="min"><xsl:value-of select="forecast-period/element[@type='air_temperature_minimum']/text()"/></td> 
              <td class="max"><xsl:value-of select="forecast-period/element[@type='air_temperature_maximum']/text()"/></td>
            </tr>      
          </xsl:for-each>
        </tbody>
      </table>
    </xsl:for-each>
  </xsl:template>
  
  <!-- templates for processing third file -->
  <xsl:template match="area">
    <!-- select the right interstate cities -->
    <xsl:if test="@description = 'Adelaide' or @description = 'Brisbane' or @description = 'Canberra' or @description = 'Darwin' or @description = 'Hobart' or @description = 'Melbourne' or @description = 'Perth' or @description = 'Sydney'">
      <tr>
        <td class="name location"><a target="_blank"><xsl:attribute name="href">/resources/static/map.html?location=<xsl:value-of select="@description"/></xsl:attribute><xsl:value-of select="@description"/></a></td>
        <td class="forecast">
          <xsl:value-of select="forecast-period/text[@type='precis']"/>
        </td>
        <td class="min"><xsl:value-of select="forecast-period/element[@type='air_temperature_minimum']/text()"/></td> 
        <td class="max"><xsl:value-of select="forecast-period/element[@type='air_temperature_maximum']/text()"/></td>
      </tr>      
    </xsl:if>
  </xsl:template>
  
  <!-- template for processing the fourth file -->
  <xsl:template match="pl:item">
    <tr>  
      <td class="event-title"><xsl:value-of select="pl:title"/></td>
      <td class="event-url"><a target="_blank"><xsl:attribute name="href"><xsl:value-of select="pl:link"/></xsl:attribute><xsl:text>Link</xsl:text></a></td>
      <td class="event-description"><xsl:value-of select="pl:description"/></td>
    </tr>
  </xsl:template>
  
  <!-- misc templates -->
  
  <!-- 
     This template takes a timestamp as input. It returns the day of week for the input date.
     The return value is a string (e.g., 'Saturday').
  -->
  <xsl:template name="getDayOfWeek">
    <xsl:param name="dateTime" />
    <xsl:param name="date" select="substring-before($dateTime,'T')" />
    <xsl:param name="year" select="substring-before($date,'-')" />
    <xsl:param name="month" select="substring-before(substring-after($date,'-'),'-')" />
    <xsl:param name="day" select="substring-after(substring-after($date,'-'),'-')" />

    <xsl:variable name="a" select="floor((14 - $month) div 12)" />
    <xsl:variable name="y" select="$year - $a" />
    <xsl:variable name="m" select="$month + 12 * $a - 2" />

    <xsl:variable name="dayIndex" select="($day + $y + floor($y div 4) - floor($y div 100) + floor($y div 400) + floor((31 * $m) div 12)) mod 7" />
    
    <xsl:choose>
      <xsl:when test="$dayIndex = 0">
        <xsl:text>Sunday</xsl:text> 
      </xsl:when>
      <xsl:when test="$dayIndex = 1">
        <xsl:text>Monday</xsl:text> 
      </xsl:when>
      <xsl:when test="$dayIndex = 2">
        <xsl:text>Tuesday</xsl:text> 
      </xsl:when>
      <xsl:when test="$dayIndex = 3">
        <xsl:text>Wednesday</xsl:text> 
      </xsl:when>
      <xsl:when test="$dayIndex = 4">
        <xsl:text>Thursday</xsl:text> 
      </xsl:when>
      <xsl:when test="$dayIndex = 5">
        <xsl:text>Friday</xsl:text> 
      </xsl:when>
      <xsl:when test="$dayIndex = 6">
        <xsl:text>Saturday</xsl:text> 
      </xsl:when>
    </xsl:choose>
  </xsl:template>
  
  <!-- 
    This template prints an img tag with the right icon URL.
    The information for matching an icon code with a particular icon can be found in bom.gov.au
   -->
  <xsl:template name="showWeatherIcon">
    <xsl:param name="imageCode" />
    <xsl:param name="iconType"/>

    <xsl:choose>
      <xsl:when test="$imageCode = 1">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/sunny.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 2">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/clear.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 3">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/partly-cloudy.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 4">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/cloudy.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 6">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/haze.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 8">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/light-rain.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 9">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/wind.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 10">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/fog.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 11">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/showers.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 12">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/rain.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 13">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/dusty.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 14">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/frost.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 15">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/snow.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 16">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/storm.png" alt="icon" />
      </xsl:when>
      <xsl:when test="$imageCode = 17">
          <img class="{$iconType}" src="resources/graphics/weather/{$iconType}-icons/light-showers.png" alt="icon" />
      </xsl:when>
    </xsl:choose>
  </xsl:template> 
</xsl:stylesheet>