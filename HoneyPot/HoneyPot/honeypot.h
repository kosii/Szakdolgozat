#ifndef HONEYPOT_H
#define HONEYPOT_H

#include <QObject>

class honeypot : public QObject
{
	Q_OBJECT

public:
	honeypot(QObject *parent);
	virtual ~honeypot();

public slots:
	void Slot1(int v);

signals:
	void Signal(int v);

private:
	
};

#endif // HONEYPOT_H
