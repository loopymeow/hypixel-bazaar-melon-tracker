# imports
import sys, time, datetime
#(pygame imports)
import pygame
from pygame.locals import *
#(beautifulsoup imports)
from bs4 import BeautifulSoup
import requests

# window settings
FPS = 60
WIDTH, HEIGHT = 800, 600
fpsClock = pygame.time.Clock()
icon = pygame.image.load('pics/icon.png') 
pygame.init()
pygame.font.init()
pygame.display.set_caption("hypixel skyblock bazaar tracker :3")

def scrapeData(ench_count):
    url_list = ["https://skyblock.finance/items/GOLD_INGOT",
                "https://skyblock.finance/items/MELON",
                "https://skyblock.finance/items/ENCHANTED_GLISTERING_MELON"]
    url_count = 0
    for url in url_list:
        if url_count < 3:
            target_index = 4
        else:
            target_index = 0
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elements_by_class = soup.find_all(class_='LabelValue_value__v87U1')
            index=0
            for element in elements_by_class:
                if index == target_index:
                    result = str(element.get_text())
                    result = result[0:len(result)-6]
                    for char in result:
                        if char == "k":
                            result = result[0:len(result)-1]
                            result = float(result)*1000
                    print(result)
                index+=1
            if url_count == 0:
                global ingot_buy
                ingot_buy = float(result)
            elif url_count == 1:
                global melon_buy
                melon_buy = float(result)
            else:
                global ench_sell
                ench_sell = float(result)
        else:
            print("Failed to retrieve the page")
        url_count += 1
        updateData(ingot_buy, melon_buy, ench_sell, ench_count)
        saveData(ingot_buy, melon_buy, ench_sell, ench_count)

def loadData():
    # ingot
    loadedIngot = getFileValue("data.txt",0)
    ingot_buy = float(loadedIngot)
    # melon
    loadedMelon = getFileValue("data.txt",1)
    melon_buy = float(loadedMelon)
    # super
    loadedSuper = getFileValue("data.txt",2)
    ench_sell = float(loadedSuper)
    # amount
    loadedAmount = getFileValue("data.txt",3)
    ench_count = float(loadedAmount)
    return ingot_buy, melon_buy, ench_sell, ench_count

def saveData(ingot_buy, melon_buy, ench_sell, ench_count):
    changeFileValue("data.txt", 0, ingot_buy)
    changeFileValue("data.txt", 1, melon_buy)
    changeFileValue("data.txt", 2, ench_sell)
    changeFileValue("data.txt", 3, ench_count)

def updateData(ingot_buy, melon_buy, ench_sell, ench_count):
    # calculations
    nugget_single_buy = ingot_buy/9
    ench_cost = (nugget_single_buy*8)+melon_buy
    ench_glis_cost = ench_cost*256
    profit_per = ench_sell - ench_glis_cost
    melon_count = ench_count*256
    materials_nuggets = melon_count*8
    materials_ingots = materials_nuggets/9
    ingot_stack = materials_ingots/64
    melon_stack = melon_count/64
    overall_spending = (materials_ingots*ingot_buy) + (melon_count*melon_buy)
    overall_revenue = ench_sell*ench_count
    overall_spending_neg = overall_spending*-1
    overall_profit = overall_revenue + overall_spending_neg

    # data list
    data_list = list()
    data_list.append(ingot_buy)
    data_list.append(melon_buy)
    data_list.append(ench_sell)
    data_list.append(nugget_single_buy)
    data_list.append(melon_buy)
    data_list.append(ench_cost)
    data_list.append(ench_glis_cost)
    data_list.append(profit_per)
    data_list.append(ench_count)
    data_list.append(melon_count)
    data_list.append(materials_nuggets)
    data_list.append(melon_count)
    data_list.append(materials_ingots)
    data_list.append(melon_count)
    data_list.append(ingot_stack)
    data_list.append(melon_stack)
    data_list.append(materials_ingots)
    data_list.append(melon_count)
    data_list.append(overall_spending)
    data_list.append(overall_revenue)
    data_list.append(overall_revenue)
    data_list.append(overall_spending_neg)
    data_list.append(overall_profit)
    return data_list, overall_profit

def changeFileValue(file, line, new):
	oldf = open(file, "r")
	all = oldf.readlines()
	all[line] = str(new) + "\n"
	oldf.close()
	newf = open(file, "w")
	newf.writelines(all)
	newf.close()

def getFileValue(file, line):
	f = open(file, "r")
	all = f.readlines()
	all = all[line]
	all = all[0:(len(all) - 1)]
	f.close()
	return all

def loadingSettings():
  # theme
  loadedtheme = getFileValue("settings.txt",0)
  if loadedtheme == "blue" or loadedtheme == "purple" or loadedtheme == "pink":
    theme = loadedtheme
  else:
    theme = "blue"
    changeFileValue("settings.txt",0 , theme)

  # scalar
  validscalar = False
  loadedscalar = getFileValue("settings.txt",1)
  if checkInt(loadedscalar) == True:
    if checkSize(loadedscalar) == True:
      scalar = int(loadedscalar)
      validscalar = True
  if validscalar == False:
    scalar = 100
    changeFileValue("settings.txt",1 , scalar)

  # details
  loadeddetails = getFileValue("settings.txt",2)
  if loadeddetails == "text" or loadeddetails == "icon":
    details = loadeddetails
  else:
    details = "text"
    changeFileValue("settings.txt", 2, details)
  
  # rerendering..
  WIDTH, HEIGHT = 800, 600
  pygame.display.set_mode((WIDTH*(scalar/100), HEIGHT*(scalar/100)))
  reloadImages(WIDTH*(scalar/100), HEIGHT*(scalar/100)) 
  return theme, scalar, details

def reloadImages(WIDTH, HEIGHT):
  global blue_text, purple_text, pink_text, blue_icon, purple_icon, pink_icon, blue_settings, purple_settings, pink_settings, cross, profit, nonprofit, icon
  blue_text = pygame.transform.smoothscale(pygame.image.load("pics/bluetext.png"), (WIDTH, HEIGHT)).convert()
  purple_text = pygame.transform.smoothscale(pygame.image.load("pics/purpletext.png"), (WIDTH, HEIGHT)).convert()
  pink_text = pygame.transform.smoothscale(pygame.image.load("pics/pinktext.png"), (WIDTH, HEIGHT)).convert()
  blue_icon = pygame.transform.smoothscale(pygame.image.load("pics/blueicon.png"), (WIDTH, HEIGHT)).convert()
  purple_icon = pygame.transform.smoothscale(pygame.image.load("pics/purpleicon.png"), (WIDTH, HEIGHT)).convert()
  pink_icon = pygame.transform.smoothscale(pygame.image.load("pics/pinkicon.png"), (WIDTH, HEIGHT)).convert()
  blue_settings = pygame.transform.smoothscale(pygame.image.load("pics/bluesettings.png"), (WIDTH, HEIGHT)).convert()
  purple_settings = pygame.transform.smoothscale(pygame.image.load("pics/purplesettings.png"), (WIDTH, HEIGHT)).convert()
  pink_settings = pygame.transform.smoothscale(pygame.image.load("pics/pinksettings.png"), (WIDTH, HEIGHT)).convert()
  cross = pygame.transform.smoothscale(pygame.image.load("pics/cross.png"), (WIDTH, HEIGHT))
  profit = pygame.transform.smoothscale(pygame.image.load("pics/profit.png"), (WIDTH, HEIGHT))
  nonprofit = pygame.transform.smoothscale(pygame.image.load("pics/nonprofit.png"), (WIDTH, HEIGHT))
  pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_icon(icon)

def checkInt(string):
  try:
      int(string)
      return True
  except ValueError:
      return False
  
def checkFloat(string):
  try:
      float(string)
      return True
  except ValueError:
      return False
  
def checkSize(string):
  string = int(string)
  if string > 1 and string < 500:
    return True
  else:
    return False
  
def drawMarketData(scalar, data_list):
  # data placement list
  data_placement_list = [
      (140, 107), (140, 163), (695, 80),
      (250, 105), (250, 163), (450, 107),
      (450, 163), (695, 170), (60, 293),
      (155, 293), (253, 293), (253, 335),
      (540, 295), (540, 333), (735, 295),
      (735, 333), (192, 455), (192, 497),
      (192, 536), (440, 422), (660, 420),
      (660, 457), (660, 500)
  ]

  # drawing the different data to the different locations on screen
  my_font = pygame.font.SysFont('segoeui', round(30*(scalar/100)))
  for index in range(0,len(data_list)):
    string = str(round(data_list[index], 2))
    if string[len(string)-2:len(string)] == ".0":
      string = string[0:len(string)-2]
    text_surface = my_font.render(string, True, (0, 0, 0))
    original_x = data_placement_list[index][0] - len(string)*7
    WINDOW.blit(text_surface, (original_x*(scalar/100), data_placement_list[index][1]*(scalar/100)))

def drawWindow(scene, theme, details, tempstring, scalar, changing, data_list, overall_profit, sync):
  WINDOW.fill((255, 255, 255))
  my_font = pygame.font.SysFont('segoeui', round(30*(scalar/100)))
  # drawing the backgound
  if scene == "main":
    if details == "text":
      if theme == "blue":
        WINDOW.blit(blue_text,(0,0))
      elif theme == "purple":
        WINDOW.blit(purple_text,(0,0))           
      else:
        WINDOW.blit(pink_text,(0,0))
    else:
      if theme == "blue":
        WINDOW.blit(blue_icon,(0,0))
      elif theme == "purple":
        WINDOW.blit(purple_icon,(0,0))           
      else:
        WINDOW.blit(pink_icon,(0,0))
    if overall_profit>=0:
      WINDOW.blit(profit,(-4,-2))
    else:
      WINDOW.blit(nonprofit,(-4,-2))
    drawMarketData(scalar, data_list)
  elif scene == "settings":
      if theme == "blue":
        WINDOW.blit(blue_settings,(0,0))
      elif theme == "purple":
        WINDOW.blit(purple_settings,(0,0))           
      else:
        WINDOW.blit(pink_settings,(0,0))
  # drawing text
  if scene == "settings":
    if changing == "size":
      # drawing demo window size to screen
      text_surface = my_font.render(tempstring+"%", True, (0, 0, 0))
      original_x = 410 - len(tempstring)*7
      WINDOW.blit(text_surface, (original_x*(scalar/100), 325*(scalar/100)))
    else:
      # drawing actual window_size to screen
      string_scalar = str(scalar) +"%"
      text_surface = my_font.render(string_scalar, True, (0, 0, 0))
      original_x = 410 - len(string_scalar)*7
      WINDOW.blit(text_surface, (original_x*(scalar/100), 325*(scalar/100)))
  if scene == "main":
     if changing != False:
        # drawing the current potential new value for a buy/sell price of an item
        text_surface = my_font.render(tempstring, True, (0, 0, 0))
        original_x = 435 - len(tempstring)*7
        WINDOW.blit(text_surface, (original_x*(scalar/100), 485*(scalar/100)))
      # drawing the sync cross
     if sync == True:
        WINDOW.blit(cross,(-4,-1))
  pygame.display.update()

def main():
  global WINDOW
  # default variables
  scene = "main"
  sync = False
  changing = False
  tempstring = ""

  # loading from files
  ingot_buy, melon_buy, ench_sell, ench_count = loadData()
  data_list, overall_profit = updateData(ingot_buy, melon_buy, ench_sell, ench_count)
  theme, scalar, details = loadingSettings()
  reloadImages(WIDTH, HEIGHT)

  # setting up display
  WINDOW = pygame.display.set_mode((WIDTH*(scalar/100), HEIGHT*(scalar/100)))
  reloadImages(WIDTH*(scalar/100), HEIGHT*(scalar/100))
  # running the application loop
  loop = True
  while loop :
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        print("mouse position clicked:",x,y)
        #SWITCHING BETWEEN MENUS
        # main clicked
        if x>0*(scalar/100) and x<175*(scalar/100) and y>0*(scalar/100) and y<50*(scalar/100):
          scene = "main"
          print("clicked main")
        # settings clicked
        if x>175*(scalar/100) and x < 335*(scalar/100) and y>0*(scalar/100) and y<50*(scalar/100):
          scene = "settings"
          print("clicked settings")
        #CLICKING IN MAIN
        if scene == "main":
            # ingot change
            if x>78*(scalar/100) and x<195*(scalar/100) and y>103*(scalar/100) and y<155*(scalar/100):
                changing = "ingot"
                print("changing ingot")
            # melon change
            if x>80*(scalar/100) and x<194*(scalar/100) and y>160*(scalar/100) and y<210*(scalar/100):
                changing = "melon"
                print("changing melon")
            # super change
            if x>629*(scalar/100) and x<771*(scalar/100) and y>80*(scalar/100) and y<127*(scalar/100):
                changing = "super"
                print("changing super")
            # amount change
            if x>15*(scalar/100) and x<108*(scalar/100) and y>298*(scalar/100) and y<334*(scalar/100):
                changing = "amount"
                print("changing amount")
            # sync change
            if x>613*(scalar/100) and x<646*(scalar/100) and y>10*(scalar/100) and y<40*(scalar/100):
                if sync == True:
                   sync = False
                else:
                   sync = True
        #CLICKING IN SETTINGS
        if scene == "settings":
            #CHANGING THEMES 
            # blue theme
            if x>100*(scalar/100) and x<255*(scalar/100) and y>130*(scalar/100) and y<240*(scalar/100):
                theme = "blue"
                changeFileValue("settings.txt", 0, theme)
                print("changed to blue theme")
            # purple theme
            if x>330*(scalar/100) and x<490*(scalar/100) and y>130*(scalar/100) and y<240*(scalar/100):
                theme = "purple"
                changeFileValue("settings.txt", 0, theme)
                print("changed to purple theme")
            # pink theme
            if x>565*(scalar/100) and x<725*(scalar/100) and y>130*(scalar/100) and y<240*(scalar/100):
                theme = "pink"
                changeFileValue("settings.txt", 0, theme)
                print("changed to pink theme")
            #CHANGING DETAILS
            # text
            if x>220*(scalar/100) and x<380*(scalar/100) and y>445*(scalar/100) and y<555*(scalar/100):
                details = "text"
                changeFileValue("settings.txt", 2, details)
                print("changed to text")
            # icon
            if x>455*(scalar/100) and x<610*(scalar/100) and y>445*(scalar/100) and y<555*(scalar/100):
                details = "icon"
                changeFileValue("settings.txt", 2, details)
                print("changed to icons")
            #CHANGING SIZE
            if x>275*(scalar/100) and x<560*(scalar/100) and y>310*(scalar/100) and y<385*(scalar/100):
                changing = "size"
                changeFileValue("settings.txt", 2, details)
                print("toggle changingsize to true")
    # keyboard inputs for the window sizing
      if changing != False:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            print("Entered text:"+tempstring)
            if changing == "size":
                if checkInt(tempstring) == True:
                    if checkSize(tempstring) == True:
                        scalar = int(tempstring)
                        reloadImages(WIDTH*(scalar/100), HEIGHT*(scalar/100))
                        changeFileValue("settings.txt", 1, scalar)
            if checkFloat(tempstring) == True:
              if float(tempstring)>=0:
                # changing ingot buy price
                if changing == "ingot":
                    ingot_buy = float(tempstring)
                    data_list, overall_profit = updateData(ingot_buy, melon_buy, ench_sell, ench_count)
                    saveData(ingot_buy, melon_buy, ench_sell, ench_count)
                    print("INGOT CHANGED")
                # changing melon buy price
                if changing == "melon":
                    melon_buy = float(tempstring)
                    data_list, overall_profit = updateData(ingot_buy, melon_buy, ench_sell, ench_count)
                    saveData(ingot_buy, melon_buy, ench_sell, ench_count)
                    print("MELON CHANGED")
                # changing enchanted glistening melon sale price
                if changing == "super":
                    ench_sell = float(tempstring)
                    data_list, overall_profit = updateData(ingot_buy, melon_buy, ench_sell, ench_count)
                    saveData(ingot_buy, melon_buy, ench_sell, ench_count)
                    print("SUPER CHANGED")
                # changing bulk craft amount
                if changing == "amount":
                    if float(tempstring) %9 == 0:
                      ench_count = float(tempstring)
                      data_list, overall_profit = updateData(ingot_buy, melon_buy, ench_sell, ench_count)
                      saveData(ingot_buy, melon_buy, ench_sell, ench_count)
                      print("AMOUNT CHANGED")
            tempstring = ""
            changing = False
            print("changed changing to false")
          elif event.key == pygame.K_BACKSPACE:
              tempstring = tempstring[:-1]
              print(tempstring)
          else:
              tempstring += event.unicode
              print(tempstring)
    # application loop
    drawWindow(scene, theme, details, tempstring, scalar, changing, data_list, overall_profit, sync)
    fpsClock.tick(FPS)
    if sync == True:
        if datetime.datetime.now().second == 0:
            print("updating data...")
            scrapeData(ench_count)
            time.sleep(1)

main()