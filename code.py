import mechanicalsoup 
import sys

def get_deed(street_number, street_password, username, password):
	browser = mechanicalsoup.StatefulBrowser()
	browser.open("https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx")

	browser.select_form()
	browser.form.set_select({
		"ctl00$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucSearchType$ddlCounty":"14", 
		"ctl00$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucSearchType$ddlSearchType":"01"
		})
	browser.submit_selected()

	browser.select_form()
	browser["ctl00$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucEnterData$txtStreenNumber"] = street_number
	browser["ctl00$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucEnterData$txtStreetName"] = street_name
	browser.form.choose_submit("ctl00$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$StepNavigationTemplateContainerID$btnStepNextButton")
	browser.submit_selected()

	page = browser.page
	ids = ["cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label42_0",
		"cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label48_0",
		"cphMainContentArea_ucSearchType_wzrdRealPropertySearch_ucDetailsSearch_dlstDetaisSearch_Label54_0"]

	deeds=[]
	for id in ids:
		deed = page.find(id=id).text.split("/")
		deed_book = deed[1].strip(' ').lstrip('0')
		deed_page = deed[2].strip(' ').lstrip('0')
		if (deed_book != '') or (deed_page != ''):
			deeds.append((deed_book, deed_page))

	while len(deeds) != 0:
		deed = deeds.pop(0)
		browser.open("https://mdlandrec.net/main/index.cfm")

		browser.select_form(nr=1)
		browser["username"] = username
		browser["password"] = password
		browser.submit_selected()
		browser.open("https://mdlandrec.net/main/dsp_search.cfm?cid=HO")

		browser.select_form(nr=1)
		browser["book"] = deeds[0][0]
		browser["StartPage"] = deeds[0][1]
		browser.form.choose_submit("NewVolume")
		browser.submit_selected()

		browser.select_form(nr=2)
		url="https://mdlandrec.net" + browser.page.select("iframe")[0]["src"]
		browser.open("url")
		with open('filename.pdf', 'wb') as outf:  
			outf.write(response.content)         

def main():
	args = sys.argv[1:]
	get_deed(args[0], args[1], args[2], args[3])

if __name__=="__main__":
	main()