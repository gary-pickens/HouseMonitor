import numpy

K = 1000
micro = .000001
<<<<<<< HEAD
nano = .000000001
pico = .000000000001

# class normal555Calculations( object ):
#     R1 = 4.5 * K
#     R2 = 33 * K
#     C = 0.01 * micro
#     V = 5.0
#     VD = 0.6
#     low = 0
#     high = 0
#     freq = 0.0
#
#     def compute( self ):
#         self.low = numpy.log( 2 ) * self.R2 * self.C
#         self.high = numpy.log( 2 ) * ( self.R1 + self.R2 ) * self.C
#         self.freq = 1 / ( numpy.log( 2 ) * self.C * ( self.R1 + ( 2 * self.R2 ) ) )
#         print 'R1 = ', self.R1
#         print 'R2 = ', self.R2
#         print 'C = ', self.C
#         print
#         print 'low time = ', self.low / 1000000
#         print 'high time = ' , self.high / 1000000
#         print 'freq = ', self.freq
#         print 'ratio = ', ( self.low / self.high ) * 100
#         print
#
#
class special555Calculations( object ):
    R1 = 2.2 * K
    R2 = 33.0 * K
    C = 1000 * micro
    V = 5.0
    VD = 0.6

    def compute( self ):
        print 'for times with a greater than 50% duty cycle'
        self.low = numpy.log( 2 ) * self.R2 * self.C
        self.high = self.R1 * self.C * numpy.log( ( ( 2 * self.V ) - ( 3 * self.VD ) ) / ( self.V - ( 3 * self.VD ) ) )
        print 'R1 = ', self.R1
        print 'R2 = ', self.R2
        print 'C = ', self.C
        print
        print 'low time = ', self.low
        print 'high time = ', self.high

n = special555Calculations()
print '555 with diode'
n.compute()

# class revised555Calculations( object ):
#     R1 = 330 * K
#     R2 = 22 * K
#     C = 0.001
#     V = 5.0
#     VD = 0.6
#     low = 0
#     high = 0
#     freq = 0.0
#
#     def compute( self ):
#         self.low = numpy.log( 2 ) * self.R2 * self.C
#         self.high = numpy.log( 2 ) * ( self.R1 + self.R2 ) * self.C
#         self.freq = 1 / ( numpy.log( 2 ) * self.C * ( self.R1 + ( 2 * self.R2 ) ) )
#         print 'R1 = ', self.R1
#         print 'R2 = ', self.R2
#         print 'C = ', self.C
#         print
#         print 'low time = ', self.low
#         print 'high time = ' , self.high
#         print 'freq = ', self.freq
#         print 'ratio = ', ( self.low / self.high ) * 100
#         print
#
# s = revised555Calculations()
# print '555'
# s.compute()
=======
nano =  .000000001
pico =  .000000000001

class normal555Calculations(object):
    R1=4.5 * K
    R2=33 * K
    C=0.01 * micro
    V=5.0
    VD=0.6
    low = 0
    high = 0
    freq = 0.0
    
    def compute(self):
        self.low=numpy.log(2) * self.R2 * self.C
        self.high=numpy.log(2) * (self.R1 + self.R2) * self.C
        self.freq = 1 / (numpy.log(2) * self.C * (self.R1 + (2 * self.R2)))
        print 'R1 = ', self.R1
        print 'R2 = ', self.R2
        print 'C = ', self.C
        print
        print 'low time = ', self.low / 1000000
        print 'high time = ' , self.high / 1000000
        print 'freq = ', self.freq
        print 'ratio = ', (self.low / self.high) * 100
        print
    
class special555Calculations(object):
    R1=330 * K
    R2=22 * K
    C=0.0001
    V=5.0
    VD=0.6

    def compute(self):
        print 'for times with a greater than 50% duty cycle'
        self.low = numpy.log(2) * self.R2 * self.C
        self.high = self.R1 * self.C * numpy.log(2*self.V - 3 * self.VD/self.V - 3 * self.VD)
        print 'R1 = ', self.R1
        print 'R2 = ', self.R2
        print 'C = ', self.C
        print
        print 'low time = ', self.low
        print 'high time = ', self.high

n = normal555Calculations()
print 'Normal 555'
n.compute()

s = special555Calculations()
print 'Special 555'
s.compute()
>>>>>>> refs/heads/monitorComputerUsage
