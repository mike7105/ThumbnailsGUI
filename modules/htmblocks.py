# -*- coding: utf-8 -*-
startHTM="""
<!DOCTYPE html><html lang="ru-RU">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta http-equiv="Content-Language" content="ru-RU"/>
		<meta http-equiv="Expires" content="-1"/>
		<meta http-equiv="Pragma" content="no-cache"/>
		<meta name="Robots" content="noindex, nofollow"/>
		<meta name="Generator" content="Interviewer Server HTML Player 1.0.23..312"/>
		<meta name="Template" content="templates\Layout_v9s.htm"/>
		<meta name="vs_targetSchema" content="http://schemas.microsoft.com/intellisense/ie5"/>
		<meta http-equiv="Page-Enter" content="blendTrans(Duration=0.5);"/>
		<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
		<title>Онлайн-опрос</title>
		<link rel="shortcut icon" href="https://www.ipsos.com/themes/custom/ipsos/favicon.ico"/>
		<link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:200,200i,300,300i,400,400i,600,600i,700,700i,900,900i&amp;subset=cyrillic"/>
		<link rel="stylesheet" type="text/css" href="https://ipsos-prod.fullstack-development.com/build/css/app.css"/>
		<link rel="stylesheet" type="text/css" href="https://ipsos-prod.fullstack-development.com/build/css/shared.css"/>
		<script type="text/javascript" src="https://ipsos-prod.fullstack-development.com/build/js/vendor.bundle.js"></script>
		<script type="text/javascript" src="https://ipsos-prod.fullstack-development.com/build/js/shared.bundle.js"></script>
		<script type="text/javascript" src="https://ipsos-prod.fullstack-development.com/build/js/app.bundle.js"></script>
		<script type="text/javascript" src="https://ipsos-prod.fullstack-development.com/build/js/ie8OrLower.js"></script>
		<link rel="stylesheet" type="text/css" href="https://survey.ipsos.ru/qst/dp726/MDD Scripts/Templates_v3/CSS/mc.css"/>
		<script type="text/javascript" src="https://yastatic.net/jquery/3.1.1/jquery.min.js"></script>
		<script type="text/javascript" src="https://survey.ipsos.ru/qst/dp726/MDD Scripts/Templates_v3/js/mc_fin.js"></script>
	</head>
	<body bgcolor="#DEDEDE" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0" style="height: 758px">
		<form name="mrForm" id="mrForm" action="/mrIWeb/mrIWeb.dll" method="post">
			<input type="hidden" name="I.Engine" value="engine7"/>
			<input type="hidden" name="I.Project" value="S2014419"/>
			<input type="hidden" name="I.Session" value="sszmwfppyxgedlbat56lg1qqgqjqaaaa"/>
			<input type="hidden" name="I.SavePoint" value="MA2"/>
			<input type="hidden" name="I.Renderer" value="HTMLPlayer"/>
			<div id="container">
				<div id="HeaderBox">
					<table border="0" width="100%" cellspacing="0" cellpadding="0">
						<tr>
							<td align="center">
								<img src="https://survey.ipsos.ru/qst/dp/_logo/ipsoslogonew.png" align="left" border="0" width="40"/>
							</td>
							<td align="right">
								<div style="height:20px;width:250px;border-width:1px;border-style:solid; font-size:xx-small">
									<table style="height: 100%; width: 100%">
										<tr><td style="width: 50%; background-color: #107FBA"/><td class="mrProgressText">50%</td>
										</tr>
									</table>
								</div>
							</td>
						</tr>
					</table>
					<div id="headerBg"></div>
				</div>
				<div class="page" id="SurroundContents">
					<div class="question select" id="SurveyContents">
						<br/>
						<div></div>
						<span class="mrQuestionText" style=""><input type="hidden" name="CustomStyle" value="MultiCol" popup="true"/>
							MA2. Многоответный вопрос в несколько колонок <br/>
							<span class="instr">ВОЗМОЖНО НЕСКОЛЬКО ОТВЕТОВ</span></span>
						<div><br/></div>
						<div></div>
						<span style="">
							<span class="mrQuestionTable" style="display:block;margin-left: 1em;">
"""

endHTM="""
							</span>
						</span>
						<div><br/></div>
						<br/>
						<div class="banner"/>
						<br/>
						<br/>
					</div>
					<div id="footerholder" class="footerholder_desktop">
						<div class="submit_div" id="buttons">
							<input type="submit" name="_NPrev" class="mrPrev" style="width: 70px;" value="Назад" alt="Назад"></input>
							<input type="submit" name="_NNext" class="mrNext" style="width: 70px;" value="Далее" alt="Далее"></input>
						</div>
					</div>
				</div>
			</div>
		</form></body>
</html>
"""

blockHTM="""
								<span id="Cell.0.{0}" style="">
									<div></div>
									<input type="checkbox" name="_QMA2_C__{1}" id="_Q0_C{2}" class="mrMultiple" style="margin-left: 1em;" value="__{3}">
										<label for="_Q0_C{4}">
											<span class="mrMultipleText" style="">
												{5}<br/><img src="{6}"/>
											</span>
										</label>
									</input>
								</span>
"""
