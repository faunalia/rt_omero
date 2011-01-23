<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="1.7.0-Trunk" minimumScale="0" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0" >
  <transparencyLevelInt>255</transparencyLevelInt>
  <renderer-v2 type="RuleRenderer" >
    <rules>
      <rule scalemaxdenom="10000000" filter=" 1:25k - oltre" symbol="0" scalemindenom="25000" />
      <rule scalemaxdenom="25000" filter=" 1:2k - 1:25k" symbol="1" scalemindenom="2000" />
      <rule scalemaxdenom="2000" filter=" 1:1 - 1:2k" symbol="2" scalemindenom="1" />
    </rules>
    <symbols>
      <symbol outputUnit="MM" alpha="1" type="fill" name="0" >
        <layer pass="0" class="CentroidFill" locked="0" />
      </symbol>
      <symbol outputUnit="MM" alpha="1" type="fill" name="1" >
        <layer pass="0" class="SimpleFill" locked="0" >
          <prop k="color" v="250,155,200,255" />
          <prop k="color_border" v="255,135,200,255" />
          <prop k="offset" v="0,0" />
          <prop k="style" v="solid" />
          <prop k="style_border" v="solid" />
          <prop k="width_border" v="0.26" />
        </layer>
      </symbol>
      <symbol outputUnit="MM" alpha="0.3921568627450981" type="fill" name="2" >
        <layer pass="0" class="SimpleFill" locked="0" >
          <prop k="color" v="250,155,200,100" />
          <prop k="color_border" v="240,110,200,100" />
          <prop k="offset" v="0,0" />
          <prop k="style" v="solid" />
          <prop k="style_border" v="solid" />
          <prop k="width_border" v="0.36" />
        </layer>
        <layer pass="0" class="MarkerLine" locked="0" >
          <prop k="interval" v="3" />
          <prop k="offset" v="0" />
          <prop k="placement" v="vertex" />
          <prop k="rotate" v="1" />
        </layer>
      </symbol>
      <symbol outputUnit="MM" alpha="1" type="fill" name="default" >
        <layer pass="0" class="SimpleFill" locked="0" >
          <prop k="color" v="30,236,236,255" />
          <prop k="color_border" v="0,0,0,255" />
          <prop k="offset" v="0,0" />
          <prop k="style" v="solid" />
          <prop k="style_border" v="solid" />
          <prop k="width_border" v="0.26" />
        </layer>
      </symbol>
      <symbol outputUnit="MM" alpha="1" type="marker" name="@0@0" >
        <layer pass="0" class="SimpleMarker" locked="0" >
          <prop k="angle" v="0" />
          <prop k="color" v="250,155,200,255" />
          <prop k="color_border" v="250,155,200,255" />
          <prop k="name" v="circle" />
          <prop k="offset" v="0,0" />
          <prop k="size" v="0.5" />
        </layer>
      </symbol>
      <symbol outputUnit="MM" alpha="0.3921568627450981" type="marker" name="@2@1" >
        <layer pass="0" class="SimpleMarker" locked="0" >
          <prop k="angle" v="0" />
          <prop k="color" v="255,76,184,255" />
          <prop k="color_border" v="0,0,0,255" />
          <prop k="name" v="circle" />
          <prop k="offset" v="0,0" />
          <prop k="size" v="1" />
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <displayfield>CODICE</displayfield>
  <label>0</label>
  <labelattributes>
    <label fieldname="" text="Etichetta" />
    <family fieldname="" name="MS Shell Dlg 2" />
    <size fieldname="" units="pt" value="12" />
    <bold fieldname="" on="0" />
    <italic fieldname="" on="0" />
    <underline fieldname="" on="0" />
    <strikeout fieldname="" on="0" />
    <color fieldname="" red="0" blue="0" green="0" />
    <x fieldname="" />
    <y fieldname="" />
    <offset x="0" y="0" units="pt" yfieldname="" xfieldname="" />
    <angle fieldname="" value="0" auto="0" />
    <alignment fieldname="" value="center" />
    <buffercolor fieldname="" red="255" blue="255" green="255" />
    <buffersize fieldname="" units="pt" value="1" />
    <bufferenabled fieldname="" on="" />
    <multilineenabled fieldname="" on="" />
    <selectedonly on="" />
  </labelattributes>
  <edittypes>
    <edittype type="0" name="CODICE" />
  </edittypes>
  <editform></editform>
  <editforminit></editforminit>
  <annotationform></annotationform>
  <attributeactions/>
  <customproperties/>
</qgis>
