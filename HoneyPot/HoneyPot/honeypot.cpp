#include "honeypot.h"

honeypot::honeypot(QObject *parent)
	: QObject(parent)
{
	QObject::connect(this, SIGNAL(honeypot::Signal(int)), this, SLOT(honeypot::Slot1(int)));
}

honeypot::~honeypot()
{

}

void honeypot::Slot1(int v){}