import goGame_main as goMain
import goGameClass as go


def generateTuples(string):
    list = []
    for i in range(0,len(string), 2):
        list.append((int(string[i]),int(string[i+1])))
    return list

def getProblems(ind):
    return problems[ind]

problems = []

# dpiecestest = generateTuples('01112122232414150503')
# # white
# apiecestest = generateTuples('00102030313233343525261606')
# dimstest = (7,7)
# availstest = generateTuples('02121304')
# eyeSpotstest = generateTuples('02121304')
# gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
# gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
# goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
# problems.append(goObject)
# go.GoGame.utility(goObject,'Def')

#0.Easy 4
# dpiecestest = [(0,0), (0, 3), (1, 2), (2, 2), (3, 1), (2, 0)]
# # white
# apiecestest = [(1,1),(0, 2), (1, 3), (2, 3), (3,3), (3, 2), (4,1), (5,2), (1, 5)]
# dimstest = (7,7)
# availstest = generateTuples('01102130405004')
# eyeSpotstest = generateTuples('0001101120210230')
dpiecestest = [(0, 3), (1, 2), (2, 2), (3, 1), (2, 0)]
# white
apiecestest = [(0, 2), (1, 3), (2, 3), (3,3), (3, 2), (4,1), (5,2), (1, 5)]
dimstest = (7,7)
availstest = generateTuples('001101102130405004')
eyeSpotstest = generateTuples('0001101120210230')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 0'
go.GoGame.utility(goObject,'Def')

#1.Another App, really easy question..
dpiecestest = generateTuples('111213151617')
# white
apiecestest = generateTuples('10182021222325262728')
dimstest = (4,10)
availstest = generateTuples('000102030405060708142434')
eyeSpotstest = generateTuples('0102030405060724')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 1'
go.GoGame.utility(goObject,'Def')

# #Easy 9
# dpiecestest = generateTuples('011112404142')
# # white
# apiecestest = generateTuples('2002131433345051525354')
# dimstest = (7,6)
# availstest = generateTuples('00103021312232')
# eyeSpotstest = generateTuples('0010203010112131')
# gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
# gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
# goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
# problems.append(goObject)
# go.GoGame.utility(goObject,'Def')

#2.Easy 13
dpiecestest = generateTuples('122223242526161707')
# white
apiecestest = generateTuples('02112132333435472728181415')
dimstest = (5,10)
availstest = generateTuples('00010304050608091336')
eyeSpotstest = generateTuples('03040506131415')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 2'
go.GoGame.utility(goObject,'Def')

#3.Easy 18
dpiecestest = generateTuples('01202122232414')
# white
apiecestest = generateTuples('10130431323334352515')
dimstest = (5,7)
availstest = generateTuples('0002030506111230')
eyeSpotstest = generateTuples('0001020310111213')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 3'
go.GoGame.utility(goObject,'Def')

#4.Easy 22
dpiecestest = generateTuples('0312232406162636')
# white
apiecestest = generateTuples('011131223334454607172737')
dimstest = (5,8)
availstest = generateTuples('0204051314152535')
eyeSpotstest = generateTuples('03040513141525')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 4'
go.GoGame.utility(goObject,'Def')

#5.Easy 27
dpiecestest = generateTuples('10115051524232')
# white
apiecestest = generateTuples('01121423334353606162')
dimstest = (8,5)
availstest = generateTuples('0020304021314122020313')
eyeSpotstest = generateTuples('203040213141')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 5'
go.GoGame.utility(goObject,'Def')

#6.Basic 19
dpiecestest = generateTuples('10112130313251')
# white
apiecestest = generateTuples('011222243343526172')
dimstest = (8,6)
availstest = generateTuples('002040414250607071')
eyeSpotstest = generateTuples('204041425060')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 6'
go.GoGame.utility(goObject,'Def')

#7.Basic 20
dpiecestest = generateTuples('1020212241516160')
# white
apiecestest = generateTuples('001112132333304252627182')
dimstest = (10,6)
availstest = generateTuples('0131324050')
eyeSpotstest = generateTuples('30314050')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 7'
go.GoGame.utility(goObject,'Def')

#8. Basic 28
dpiecestest = generateTuples('10121323303132')
# white
apiecestest = generateTuples('01030414243433404142')
dimstest = (8,6)
availstest = generateTuples('000211202122')
eyeSpotstest = generateTuples('000211202122')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 8'
go.GoGame.utility(goObject,'Def')

#9. Basic 29
dpiecestest = generateTuples('2021314152536061')
# white
apiecestest = generateTuples('1112222430323454646362717082')
dimstest = (10,6)
availstest = generateTuples('000140505142')
eyeSpotstest = generateTuples('30405051')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 9'
go.GoGame.utility(goObject,'Def')

#10. Basic 32
dpiecestest = generateTuples('2131324252626150')
# white
apiecestest = generateTuples('111222243343546473727160')
dimstest = (9,6)
availstest = generateTuples('0010203040415170')
eyeSpotstest = generateTuples('4051413020')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 10'
go.GoGame.utility(goObject,'Def')

#11. Basic 34
dpiecestest = generateTuples('0212223031')
# white
apiecestest = generateTuples('0313233332424140')
dimstest = (6,5)
availstest = generateTuples('000110112021')
eyeSpotstest = generateTuples('20210001111002')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 11'
go.GoGame.utility(goObject,'Def')

#12. Easy 46
dpiecestest = generateTuples('03111213203132')
# white
apiecestest = generateTuples('01041424303340414243')
dimstest = (6,6)
availstest = generateTuples('021021222300')
eyeSpotstest = generateTuples('01000210212223')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 12'
go.GoGame.utility(goObject,'Def')

#13. Intermediate 7 
dpiecestest = generateTuples('0211223241')
# white
apiecestest = generateTuples('001213233343525150')
dimstest = (7,6)
availstest = generateTuples('011020213031404203')
eyeSpotstest = generateTuples('011020213031')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 13'
go.GoGame.utility(goObject,'Def')

#14. Intermediate 22
dpiecestest = generateTuples('1215162325333435')
# white
apiecestest = generateTuples('11172122262732424344454647')
dimstest = (6,9)
availstest = generateTuples('00010203040506070813142436')
eyeSpotstest = generateTuples('0203040506131424')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 14'
go.GoGame.utility(goObject,'Def')

#15. Easy 39
dpiecestest = generateTuples('11213141516171')
# white
apiecestest = generateTuples('0102101323303343505262728182')
dimstest = (10,5)
availstest = generateTuples('00122022324042607080')
eyeSpotstest = generateTuples('1020304050607080')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
print 'Game 15'
go.GoGame.utility(goObject,'Def')

#16.Easy 5
dpiecestest = generateTuples('12223141')
# white
apiecestest = generateTuples('15132332425162')
dimstest = (7,6)
availstest = generateTuples('00011011212030405060030405')
eyeSpotstest = generateTuples('00011011202130')
gametest = [apiecestest, dpiecestest, availstest, eyeSpotstest, dimstest]
gamestatetest = goMain.generateInitialState(gametest[0], gametest[1], gametest[2], gametest[3], gametest[4])
goObject = go.GoGame(gamestatetest.player, gamestatetest.moves, gamestatetest.board, gamestatetest.connectedPieces, gamestatetest.survivalState, gamestatetest.eyes)
problems.append(goObject)
go.GoGame.utility(goObject,'Def')

#GpAndroid
#1289
