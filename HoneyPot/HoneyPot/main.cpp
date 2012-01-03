#include <iostream>

#include <QtCore/QCoreApplication>

#include "honeypot.h"

int main(int argc, char *argv[])
{
	QCoreApplication a(argc, argv);
	honeypot hp(0);
	hp.metaObject();
	return a.exec();
}