#include <iostream>

#include <QtCore/QCoreApplication>

#include "honeypot.h"

int main(int argc, char *argv[])
{
	QCoreApplication a(argc, argv);
	honeypot hp(0);
	honeypot z(0);
	hp.metaObject();
	printf("kaka\n");
	hp.emitSignal();
	z.emitSignal();
	return a.exec();
}