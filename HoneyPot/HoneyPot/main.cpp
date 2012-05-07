#include <iostream>

#include <QtCore/QCoreApplication>

#include "honeypot.h"
#include "no_signals.h"

int main(int argc, char *argv[])
{
	QCoreApplication a(argc, argv);
	honeypot hp(0);
	honeypot z(0);
	no_signals ns(0);
	hp.metaObject();
	hp.qt_metacall(2, 0, 5);
	printf("kaka\n");
	ns.metaObject();
	hp.emitSignal();
	z.emitSignal();
	return a.exec();
}