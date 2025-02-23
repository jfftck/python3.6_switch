from switch import Switch


def test(a):
  output = []
  
  with Switch(a) as case:
    with case(0):
      output.append(0)
      
    with case(1):
      output.append(1)
      
    with case.fall(2):
      output.append(2)
      
    with case.fall(3):
      output.append(3)
      
    with case(4):
      output.append(4)
      
    with case.fall(5):
      output.append(5)
      
    with case.default():
      output.append('default')
      
  return '\n'.join(['test({}):'.format(a)] + ['\t{}'.format(x) for x in [', '.join([str(x) for x in output])]])


def test2(a):
  output = []
  err = []

  with Switch(str(a)) as case:
    with case('0'):
      output.append(repr('0'))

    with case.fall('1'):
      output.append(repr('1'))

    with case('2'):
      output.append(repr('2'))

    with case.fall('3'):
      output.append(repr('3'))

    with case.fall('4'):
      output.append(repr('4'))

    with case.fall('5'):
      output.append(repr('5'))

    with case('6'):
      output.append(repr('6'))

    with case.fall('7'):
      output.append(repr('7'))

    with case('8'):
      output.append(repr('8'))

    with case.default():
      output.append('default')
      
    try:
      with case('10'):
        pass
    except Exception as e:
      err.append(str(e))

  return '\n'.join(['test2({}):'.format(a)] + ['\t{}'.format(x) for x in [', '.join([str(x) for x in output])] + err])


for a in range(10):
  print (test(a))
  print (test2(a))